#!/usr/bin/env python3
"""
Flask app for rendering GitHub repos to single HTML pages.
Refactored for better code structure and maintainability.
"""

from flask import Flask, request, jsonify, render_template_string
import tempfile
import shutil
import pathlib
import logging

# Local imports
from core.repo_to_single_page import collect_files, build_html, MAX_DEFAULT_BYTES
from core.github_api import fetch_github_repo, GitHubAPIError
from core.templates import INDEX_TEMPLATE, ERROR_TEMPLATE
from core.utils import parse_github_url, validate_github_url, create_repo_id, create_repo_path

# Configure Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store rendered HTML temporarily (in production, use Redis/database)
rendered_pages = {}


@app.route('/')
def index():
    """Render the main page with form to submit GitHub URL."""
    return render_template_string(INDEX_TEMPLATE)


@app.route('/render', methods=['POST'])
def render_repo():
    """Process GitHub repository rendering request."""
    try:
        data = request.get_json()
        if not data or 'repo_url' not in data:
            return jsonify({'error': 'repo_url is required'}), 400
        
        repo_url = data['repo_url']
        max_bytes = data.get('max_bytes', MAX_DEFAULT_BYTES)
        
        # Validate GitHub URL
        if not validate_github_url(repo_url):
            return jsonify({'error': 'Only valid GitHub URLs are supported'}), 400
        
        # Parse URL to get owner and repo
        owner, repo = parse_github_url(repo_url)
        repo_id = create_repo_id(owner, repo)
        repo_path = create_repo_path(owner, repo)
        
        # Check if already cached
        if repo_id in rendered_pages:
            logger.info(f"Serving cached version of {repo_url}")
            return jsonify({
                'success': True,
                'redirect_url': f'/{repo_path}',
                'stats': rendered_pages[repo_id]['stats'],
                'cached': True
            })
        
        # Render the repository
        html_content, stats = _render_repository(repo_url, max_bytes)
        
        # Cache the result
        rendered_pages[repo_id] = {
            'html': html_content,
            'stats': stats,
            'repo_url': repo_url
        }
        
        return jsonify({
            'success': True,
            'redirect_url': f'/{repo_path}',
            'stats': stats
        })
        
    except GitHubAPIError as e:
        logger.error(f"GitHub API error: {str(e)}")
        return jsonify({'error': f'GitHub API error: {str(e)}'}), 400
    except Exception as e:
        logger.error(f"Error rendering repository: {str(e)}")
        return jsonify({'error': str(e)}), 500


def _render_repository(repo_url: str, max_bytes: int):
    """
    Internal function to render a repository.
    
    Returns:
        Tuple of (html_content, stats)
    """
    tmpdir = tempfile.mkdtemp(prefix="rendergit_")
    repo_dir = pathlib.Path(tmpdir, "repo")
    
    try:
        logger.info(f"Fetching {repo_url}")
        head = fetch_github_repo(repo_url, repo_dir)
        
        logger.info(f"Scanning files in {repo_dir}")
        infos = collect_files(repo_dir, max_bytes)
        
        logger.info("Generating HTML")
        html_content = build_html(repo_url, repo_dir, head, infos)
        
        stats = {
            'total_files': len(infos),
            'rendered_files': sum(1 for i in infos if i.decision.include),
            'skipped_files': sum(1 for i in infos if not i.decision.include),
            'commit': head[:8]
        }
        
        return html_content, stats
        
    finally:
        # Clean up temporary directory
        shutil.rmtree(tmpdir, ignore_errors=True)


@app.route('/<owner>/<repo>')
@app.route('/<owner>/<repo>/')
def render_github_repo_direct(owner, repo):
    """Direct GitHub repository rendering via URL path."""
    try:
        # Validate owner/repo format
        if not owner or not repo or '/' in owner or '/' in repo:
            return _render_error("Invalid repository path", f"/{owner}/{repo}")
        
        github_url = f"https://github.com/{owner}/{repo}"
        repo_id = create_repo_id(owner, repo)
        
        # Check if already rendered
        if repo_id in rendered_pages:
            logger.info(f"Serving cached version of {github_url}")
            return rendered_pages[repo_id]['html']
        
        # Render the repository
        logger.info(f"Direct rendering {github_url}")
        html_content, stats = _render_repository(github_url, MAX_DEFAULT_BYTES)
        
        # Cache the result
        rendered_pages[repo_id] = {
            'html': html_content,
            'stats': stats,
            'repo_url': github_url
        }
        
        return html_content
        
    except GitHubAPIError as e:
        logger.error(f"GitHub API error for {github_url}: {str(e)}")
        return _render_error(f"Failed to fetch repository: {str(e)}", github_url), 404
    except Exception as e:
        logger.error(f"Error rendering {github_url}: {str(e)}")
        return _render_error(f"Error rendering repository: {str(e)}", github_url), 500


def _render_error(error_message: str, repo_url: str):
    """Render error page with consistent styling."""
    return render_template_string(
        ERROR_TEMPLATE, 
        error=error_message, 
        repo_url=repo_url
    )


@app.route('/view/<repo_id>')
def view_rendered_repo(repo_id):
    """Legacy route - redirect to clean URL format."""
    if repo_id in rendered_pages:
        # Extract owner/repo from stored data
        repo_url = rendered_pages[repo_id]['repo_url']
        try:
            owner, repo = parse_github_url(repo_url)
            from flask import redirect
            return redirect(f'/{owner}/{repo}', code=301)
        except ValueError:
            pass
    
    return "Repository not found or expired. Please render it again.", 404

@app.route('/health/')
@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'cached_repos': len(rendered_pages)})


if __name__ == '__main__':
    app.run(debug=True)
