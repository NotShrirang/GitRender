"""
HTML templates for the Flask app.
Separated from main logic for better maintainability.
"""

# Main form template
INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RenderGit - GitHub Repository to Single Page</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #24292f;
            background-color: #ffffff;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3em;
            font-weight: 600;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .header p {
            font-size: 1.2em;
            color: #656d76;
            margin-bottom: 30px;
        }
        
        .form-container {
            background: #f6f8fa;
            border: 1px solid #d0d7de;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #24292f;
        }
        
        input[type="url"], input[type="number"] {
            width: 100%;
            padding: 12px 16px;
            border: 1px solid #d0d7de;
            border-radius: 6px;
            font-size: 16px;
            transition: border-color 0.2s;
        }
        
        input[type="url"]:focus, input[type="number"]:focus {
            outline: none;
            border-color: #0969da;
            box-shadow: 0 0 0 3px rgba(9, 105, 218, 0.1);
        }
        
        .submit-btn {
            width: 100%;
            padding: 12px 24px;
            background: #2da44e;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .submit-btn:hover {
            background: #2c974b;
        }
        
        .submit-btn:disabled {
            background: #8c959f;
            cursor: not-allowed;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
            color: #656d76;
        }
        
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #2da44e;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .error {
            background: #ff1744;
            color: white;
            padding: 12px 16px;
            border-radius: 6px;
            margin: 20px 0;
            display: none;
        }
        
        .success {
            background: #2da44e;
            color: white;
            padding: 12px 16px;
            border-radius: 6px;
            margin: 20px 0;
            display: none;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }
        
        .feature {
            background: white;
            border: 1px solid #d0d7de;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }
        
        .feature-icon {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .feature h3 {
            margin-bottom: 10px;
            color: #24292f;
        }
        
        .feature p {
            color: #656d76;
            font-size: 0.9em;
        }
        
        .footer {
            text-align: center;
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid #d0d7de;
            color: #656d76;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 RenderGit</h1>
            <p>Flatten any GitHub repository into a single, searchable HTML page</p>
        </div>
        
        <div class="form-container">
            <form id="renderForm">
                <div class="form-group">
                    <label for="repo_url">GitHub Repository URL</label>
                    <input 
                        type="url" 
                        id="repo_url" 
                        name="repo_url" 
                        placeholder="https://github.com/owner/repository"
                        required
                    >
                </div>
                
                <div class="form-group">
                    <label for="max_bytes">Max File Size (bytes)</label>
                    <input 
                        type="number" 
                        id="max_bytes" 
                        name="max_bytes" 
                        value="51200"
                        min="1024"
                        step="1024"
                    >
                </div>
                
                <button type="submit" class="submit-btn" id="submitBtn">
                    Render Repository
                </button>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                Processing repository... This may take a moment.
            </div>
            
            <div class="error" id="error"></div>
            <div class="success" id="success"></div>
        </div>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">👤</div>
                <h3>Human View</h3>
                <p>Browse with syntax highlighting and sidebar navigation</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🤖</div>
                <h3>LLM View</h3>
                <p>Copy entire codebase as CXML text for AI analysis</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🔍</div>
                <h3>Search Friendly</h3>
                <p>Use Ctrl+F to find anything across all files</p>
            </div>
            <div class="feature">
                <div class="feature-icon">📱</div>
                <h3>Responsive</h3>
                <p>Works perfectly on desktop and mobile devices</p>
            </div>
        </div>
        
        <div class="footer">
            <p>Built with Flask • Deploy on Vercel • Open Source</p>
        </div>
    </div>

    <script>
        document.getElementById('renderForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const error = document.getElementById('error');
            const success = document.getElementById('success');
            
            const repoUrl = document.getElementById('repo_url').value;
            const maxBytes = parseInt(document.getElementById('max_bytes').value);
            
            // Reset states
            error.style.display = 'none';
            success.style.display = 'none';
            loading.style.display = 'block';
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
            
            try {
                const response = await fetch('/render', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        repo_url: repoUrl,
                        max_bytes: maxBytes
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Show success message
                    success.innerHTML = `
                        Successfully rendered $${data.stats.rendered_files} files ($${data.stats.skipped_files} skipped).<br>
                        Redirecting to rendered repository...
                    `;
                    success.style.display = 'block';
                    
                    // Auto-redirect in the same window after a short delay
                    setTimeout(() => {
                        window.location.href = data.redirect_url;
                    }, 1500);
                } else {
                    error.textContent = data.error || 'An error occurred';
                    error.style.display = 'block';
                }
            } catch (err) {
                error.textContent = 'Network error: ' + err.message;
                error.style.display = 'block';
            } finally {
                loading.style.display = 'none';
                submitBtn.disabled = false;
                submitBtn.textContent = 'Render Repository';
            }
        });
    </script>
</body>
</html>
'''

# Error template for direct repository access
ERROR_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RenderGit - Error</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #24292f;
            background-color: #ffffff;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        
        .error-container {
            max-width: 600px;
            text-align: center;
            padding: 40px;
            background: #f6f8fa;
            border: 1px solid #d0d7de;
            border-radius: 12px;
        }
        
        .error-icon {
            font-size: 4em;
            margin-bottom: 20px;
        }
        
        h1 {
            color: #d1242f;
            margin-bottom: 20px;
        }
        
        .error-message {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #d1242f;
            margin: 20px 0;
            text-align: left;
        }
        
        .back-button {
            display: inline-block;
            padding: 12px 24px;
            background: #2da44e;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            margin-top: 20px;
        }
        
        .back-button:hover {
            background: #2c974b;
        }
        
        .repo-link {
            color: #0969da;
            text-decoration: none;
            font-weight: 600;
        }
        
        .repo-link:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">❌</div>
        <h1>Repository Not Found</h1>
        <p>Unable to render the repository: <a href="{{ repo_url }}" class="repo-link" target="_blank">{{ repo_url }}</a></p>
        
        <div class="error-message">
            <strong>Error:</strong> {{ error }}
        </div>
        
        <p>Please check that:</p>
        <ul style="text-align: left; margin: 20px 0; padding-left: 20px;">
            <li>The repository exists and is public</li>
            <li>The owner and repository name are spelled correctly</li>
            <li>You have internet connectivity</li>
        </ul>
        
        <a href="/" class="back-button">← Back to Home</a>
    </div>
</body>
</html>
'''
