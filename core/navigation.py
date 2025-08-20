"""
Enhanced HTML renderer with clean topbar navigation.
Separated from the main repo_to_single_page.py for better structure.
"""

import html
from pathlib import Path
from typing import List
from pygments.formatters import HtmlFormatter

def add_navigation_bar(repo_url: str) -> str:
    """Generate the top navigation bar HTML."""
    return f'''
<!-- Top Navigation Bar -->
<nav class="top-nav">
  <a href="/" class="nav-brand">
    <span class="brand-icon">🔧</span>
    <span>GitRender</span>
  </a>
  <div class="nav-actions">
    <a href="{html.escape(repo_url)}" class="nav-btn" target="_blank" rel="noopener">
      <span>📂</span>
      <span>View on GitHub</span>
    </a>
    <a href="/" class="nav-btn primary">
      <span>🏠</span>
      <span>Home</span>
    </a>
  </div>
</nav>
'''

def get_navigation_styles() -> str:
    """Generate CSS styles for the top navigation."""
    return '''
  /* Top Navigation Bar */
  .top-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: var(--bg-primary);
    border-bottom: 1px solid var(--border-light);
    z-index: 1000;
    display: flex;
    align-items: center;
    padding: 0 24px;
    box-shadow: var(--shadow-sm);
  }

  .nav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    font-weight: 600;
    font-size: 1.1rem;
    color: var(--text-primary);
    text-decoration: none;
  }

  .nav-brand:hover {
    color: var(--text-accent);
  }

  .nav-brand .brand-icon {
    font-size: 1.5rem;
  }

  .nav-actions {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .nav-btn {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: var(--bg-secondary);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 0.875rem;
    font-weight: 500;
    transition: all 0.2s ease;
  }

  .nav-btn:hover {
    background: var(--bg-tertiary);
    border-color: var(--border-medium);
    color: var(--text-primary);
    transform: translateY(-1px);
  }

  .nav-btn.primary {
    background: var(--primary-gradient);
    border-color: transparent;
    color: white;
  }

  .nav-btn.primary:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-md);
  }
'''

def get_mobile_navigation_styles() -> str:
    """Generate mobile-specific navigation styles."""
    return '''
  @media (max-width: 480px) {
    .top-nav {
      padding: 0 16px;
    }
    
    .nav-brand {
      font-size: 1rem;
      gap: 8px;
    }
    
    .nav-brand .brand-icon {
      font-size: 1.3rem;
    }
    
    .nav-actions {
      gap: 12px;
    }
    
    .nav-btn {
      padding: 6px 12px;
      font-size: 0.8rem;
    }
    
    .nav-btn span:last-child {
      display: none; /* Hide text labels on very small screens */
    }
  }
'''

def get_body_adjustments() -> str:
    """Get CSS adjustments for body to account for fixed top nav."""
    return '''
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    margin: 0; 
    padding: 0; 
    padding-top: 60px; /* Account for fixed top nav */
    line-height: 1.6;
    color: var(--text-primary);
    background: var(--bg-secondary);
    font-size: 14px;
  }
'''

def get_sidebar_adjustments() -> str:
    """Get CSS adjustments for sidebar to account for fixed top nav."""
    return '''
  #sidebar {
    position: sticky; 
    top: 60px; /* Account for fixed top nav */
    align-self: start;
    height: calc(100vh - 60px); /* Subtract top nav height */
    overflow: auto;
    background: var(--bg-sidebar);
    border-right: 2px solid var(--border-light);
    backdrop-filter: blur(10px);
    box-shadow: var(--shadow-lg);
  }
'''

def get_mobile_nav_adjustments() -> str:
    """Get CSS adjustments for mobile navigation."""
    return '''
    .mobile-nav {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 1rem;
      background: var(--bg-primary);
      border-bottom: 1px solid var(--border-light);
      position: sticky;
      top: 60px; /* Account for fixed top nav */
      z-index: 100;
      box-shadow: var(--shadow-sm);
    }
'''
