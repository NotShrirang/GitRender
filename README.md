# 🚀 GitRender

> A vibe coded extension to [@karpathy](https://github.com/karpathy)'s rendergit

<div align="center">

**Transform any GitHub repository into a single, searchable HTML page**

_Perfect for code review, exploration, and instant Ctrl+F across entire codebases_

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FNotShrirang%2FGitRender)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

[🌐 **Try Live Demo**](https://gitrender.vercel.app) · [📖 Documentation](#usage) · [🐛 Report Issues](https://github.com/NotShrirang/GitRender/issues)

</div>

---

## ✨ What is GitRender?

GitRender flattens any GitHub repository into a **single, searchable HTML page** with beautiful syntax highlighting and intuitive navigation. No more clicking through complex file hierarchies—just pure, instant access to all the code you need.

### 🎯 Perfect for:

- **Code Review**: See the entire codebase at once
- **Learning**: Explore open-source projects effortlessly
- **AI Analysis**: Export codebases in LLM-friendly format
- **Documentation**: Quick reference for project structure
- **Research**: Compare implementations across multiple files

---

## 🚀 Quick Start

### 🌐 Web Interface (Recommended)

Simply visit our hosted version and paste any GitHub repository URL:

**[🌐 GitRender Web App](https://your-vercel-deployment.vercel.app)**

### 💻 Command Line Interface

#### Installation

```bash
# Clone the repository
git clone https://github.com/NotShrirang/GitRender.git
cd GitRender

# Or with uv (recommended)
uv venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
uv pip install -r requirements.txt
```

## ✨ Features

### 🎨 **Dual View Modes**

- **👤 Human View**: Beautiful interface with syntax highlighting and navigation
- **🤖 LLM View**: Raw CXML format perfect for AI code analysis

### 🔍 **Smart Code Processing**

- **Syntax highlighting** for 200+ programming languages via Pygments
- **Markdown rendering** for documentation files
- **Smart filtering** automatically skips binaries and oversized files
- **File size optimization** with configurable limits

### 🧭 **Intuitive Navigation**

- **Directory tree** overview with expandable folders
- **Sidebar navigation** with file links and sizes
- **Jump-to-file** functionality
- **Search-friendly** - use Ctrl+F to find anything across all files

### 📱 **Modern Design**

- **Responsive layout** works on desktop, tablet, and mobile
- **Clean, minimal interface** focuses on the code
- **Fast loading** with optimized HTML output
- **Accessible** design following web standards

---

## 🔧 Technical Details

### Architecture

- **Backend**: Flask web application
- **Frontend**: Responsive HTML with modern CSS/JS
- **Deployment**: Optimized for Vercel serverless functions
- **Code Processing**: Python with Pygments and Markdown libraries

### File Processing

- Supports text files up to 50KB by default (configurable)
- Automatically detects and skips binary files
- Processes common code files, documentation, and configuration files
- Maintains original file structure and relationships

### Performance

- Efficient temporary file handling
- Optimized HTML generation
- Smart caching for repeated requests
- Maximum 60-second processing time on Vercel

---

## 🛠️ Development

### Project Structure

```
GitRender/
├── app.py              # Flask web application
├── index.py            # Vercel entry point
├── requirements.txt    # Python dependencies
├── vercel.json        # Vercel deployment configuration
├── core/              # Core functionality
│   ├── github_api.py      # GitHub API integration
│   ├── navigation.py      # Navigation utilities
│   ├── repo_to_single_page.py  # Main rendering logic
│   ├── templates.py       # HTML templates
│   └── utils.py           # Utility functions
└── README.md          # This file
```

### Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Issues and Support

- 🐛 [Report bugs](https://github.com/NotShrirang/GitRender/issues)
- 💡 [Request features](https://github.com/NotShrirang/GitRender/issues)
- 💬 [Join discussions](https://github.com/NotShrirang/GitRender/discussions)

---

## 📄 License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Original concept and implementation** by [@karpathy](https://github.com/karpathy) - this project is based on his excellent [rendergit](https://github.com/karpathy/rendergit) tool
- Inspired by the need for better code exploration tools
- Built with [Pygments](https://pygments.org/) for syntax highlighting
- Uses [Python-Markdown](https://python-markdown.github.io/) for documentation rendering
- Deployed on [Vercel](https://vercel.com/) for fast, global access

---

<div align="center">

**Made with ❤️ for developers who love exploring code**

[⭐ Star this repo](https://github.com/NotShrirang/GitRender) if GitRender helped you!

</div>
