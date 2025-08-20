"""
GitHub API-based repository fetcher for serverless environments.
This replaces git clone functionality for Vercel deployment.
"""

import requests
import zipfile
import tempfile
import pathlib
import io
import base64
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class GitHubAPIError(Exception):
    """Exception for GitHub API related errors."""
    pass

def parse_github_url(url: str) -> tuple[str, str]:
    """Parse GitHub URL to extract owner and repo name."""
    url = url.rstrip('/')
    if url.endswith('.git'):
        url = url[:-4]
    
    if not url.startswith('https://github.com/'):
        raise ValueError("URL must be a GitHub repository URL")
    
    parts = url.replace('https://github.com/', '').split('/')
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL format")
    
    return parts[0], parts[1]

def fetch_repo_archive(owner: str, repo: str, target_dir: pathlib.Path) -> str:
    """
    Fetch repository archive from GitHub and extract to target directory.
    Returns the commit SHA.
    """
    # First, get the default branch and latest commit
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    
    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        repo_info = response.json()
        
        default_branch = repo_info.get('default_branch', 'main')
        
        # Get the latest commit SHA
        commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{default_branch}"
        response = requests.get(commits_url, timeout=30)
        response.raise_for_status()
        commit_info = response.json()
        commit_sha = commit_info['sha']
        
        # Download the archive
        archive_url = f"https://github.com/{owner}/{repo}/archive/{default_branch}.zip"
        response = requests.get(archive_url, timeout=60)
        response.raise_for_status()
        
        # Extract the archive
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(target_dir.parent)
            
            # The extracted folder will be named repo-branch, move contents to target_dir
            extracted_folder = target_dir.parent / f"{repo}-{default_branch}"
            if extracted_folder.exists():
                if target_dir.exists():
                    import shutil
                    shutil.rmtree(target_dir)
                extracted_folder.rename(target_dir)
            else:
                # Try with master branch naming
                extracted_folder = target_dir.parent / f"{repo}-master"
                if extracted_folder.exists():
                    if target_dir.exists():
                        import shutil
                        shutil.rmtree(target_dir)
                    extracted_folder.rename(target_dir)
        
        logger.info(f"Successfully fetched {owner}/{repo} at commit {commit_sha[:8]}")
        return commit_sha
        
    except requests.exceptions.RequestException as e:
        raise GitHubAPIError(f"Failed to fetch repository: {str(e)}")
    except zipfile.BadZipFile as e:
        raise GitHubAPIError(f"Failed to extract repository archive: {str(e)}")
    except Exception as e:
        raise GitHubAPIError(f"Unexpected error: {str(e)}")

def fetch_github_repo(repo_url: str, target_dir: pathlib.Path) -> str:
    """
    Main function to fetch a GitHub repository using the API.
    Returns the commit SHA.
    """
    owner, repo = parse_github_url(repo_url)
    return fetch_repo_archive(owner, repo, target_dir)

# For compatibility with existing code
def git_clone_api(url: str, dst: str) -> None:
    """Git clone replacement using GitHub API."""
    target_path = pathlib.Path(dst)
    fetch_github_repo(url, target_path)

def git_head_commit_api(repo_url: str) -> str:
    """Get the HEAD commit SHA using GitHub API."""
    try:
        owner, repo = parse_github_url(repo_url)
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        repo_info = response.json()
        
        default_branch = repo_info.get('default_branch', 'main')
        
        commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits/{default_branch}"
        response = requests.get(commits_url, timeout=30)
        response.raise_for_status()
        commit_info = response.json()
        
        return commit_info['sha']
    except Exception:
        return "(unknown)"
