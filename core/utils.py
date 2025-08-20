"""
Utility functions for the GitRender Flask app.
"""

import re
from typing import Tuple


def parse_github_url(url: str) -> Tuple[str, str]:
    """
    Parse GitHub URL to extract owner and repo name.
    
    Args:
        url: GitHub repository URL
        
    Returns:
        Tuple of (owner, repo_name)
        
    Raises:
        ValueError: If URL is not a valid GitHub repository URL
    """
    url = url.rstrip('/')
    if url.endswith('.git'):
        url = url[:-4]
    
    if not url.startswith('https://github.com/'):
        raise ValueError("URL must be a GitHub repository URL")
    
    # Extract owner/repo from URL
    path_part = url.replace('https://github.com/', '')
    parts = path_part.split('/')
    
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL format")
    
    return parts[0], parts[1]


def create_repo_id(owner: str, repo: str) -> str:
    """Create a safe repository ID for internal use."""
    return f"{owner}_{repo}"


def create_repo_path(owner: str, repo: str) -> str:
    """Create a clean repository path for URLs."""
    return f"{owner}/{repo}"


def validate_github_url(url: str) -> bool:
    """
    Validate if the provided URL is a GitHub repository URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid GitHub URL, False otherwise
    """
    try:
        parse_github_url(url)
        return True
    except ValueError:
        return False


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage/display.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove/replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Limit length
    if len(filename) > 100:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        name = name[:90]
        filename = f"{name}.{ext}" if ext else name
    
    return filename


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human readable size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    if i == 0:
        return f"{int(size)} {size_names[i]}"
    else:
        return f"{size:.1f} {size_names[i]}"


def truncate_commit_hash(commit_hash: str, length: int = 8) -> str:
    """
    Truncate commit hash to specified length.
    
    Args:
        commit_hash: Full commit hash
        length: Length to truncate to (default: 8)
        
    Returns:
        Truncated commit hash
    """
    if not commit_hash or commit_hash == "(unknown)":
        return commit_hash
    
    return commit_hash[:length]
