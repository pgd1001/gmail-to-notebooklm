# Installation Guide

Complete installation instructions for the Gmail to NotebookLM converter.

## Prerequisites

- **Python 3.9 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (Python package installer - included with Python 3.4+)
- **Git** (optional, for cloning the repository)
- **Google account** with Gmail access
- **Google Cloud Project** with Gmail API enabled (see [OAUTH_SETUP.md](OAUTH_SETUP.md))

## Quick Installation

```bash
# 1. Clone or download the repository
git clone https://github.com/yourusername/gmail-to-notebooklm.git
cd gmail-to-notebooklm

# 2. Create a virtual environment (recommended)
python -m venv .venv

# 3. Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install the package in development mode
pip install -e .

# 6. Set up OAuth credentials (see OAUTH_SETUP.md)
# Place your credentials.json in the project root

# 7. Test the installation
gmail-to-notebooklm --help
```

## Detailed Installation Steps

### Step 1: Check Python Installation

Verify Python is installed and meets the version requirement:

```bash
python --version
# Should show Python 3.9.0 or higher
```

If Python is not installed or the version is too old, download and install from [python.org](https://www.python.org/downloads/).

### Step 2: Get the Source Code

**Option A: Clone with Git (recommended)**

```bash
git clone https://github.com/yourusername/gmail-to-notebooklm.git
cd gmail-to-notebooklm
```

**Option B: Download ZIP**

1. Download the ZIP file from the repository
2. Extract to a directory of your choice
3. Open a terminal/command prompt in that directory

### Step 3: Create a Virtual Environment

Using a virtual environment is **strongly recommended** to avoid dependency conflicts:

```bash
# Create virtual environment
python -m venv .venv

# This creates a .venv directory in your project
```

**Why use a virtual environment?**
- Isolates project dependencies from system Python packages
- Prevents version conflicts with other Python projects
- Makes the project portable and reproducible

### Step 4: Activate the Virtual Environment

**Windows (Command Prompt):**
```cmd
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

You should see `(.venv)` at the beginning of your command prompt, indicating the virtual environment is active.

### Step 5: Install Dependencies

With the virtual environment activated:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- Google API client libraries
- OAuth authentication libraries
- HTML parsing and Markdown conversion tools
- CLI utilities

### Step 6: Install the Package

Install the package in editable/development mode:

```bash
pip install -e .
```

This makes the `gmail-to-notebooklm` command available system-wide (within your virtual environment).

### Step 7: Configure OAuth 2.0

Follow the complete guide in [OAUTH_SETUP.md](OAUTH_SETUP.md) to:
1. Create a Google Cloud Project
2. Enable the Gmail API
3. Configure OAuth consent screen
4. Download `credentials.json`
5. Place `credentials.json` in the project root directory

### Step 8: Verify Installation

Test that everything is installed correctly:

```bash
# Check the CLI is available
gmail-to-notebooklm --version

# View help
gmail-to-notebooklm --help
```

### Step 9: First Run Authentication

On your first run, you'll need to authenticate:

```bash
gmail-to-notebooklm --label "Test" --output-dir "./test_output"
```

This will:
1. Open your default web browser
2. Prompt you to sign in to Google
3. Ask for permission to read Gmail (readonly access)
4. Save a `token.json` file for future use

## Development Installation

If you're contributing to the project or want to run tests:

```bash
# Install with development dependencies
pip install -e ".[dev]"

# This includes pytest, black, flake8, mypy, etc.
```

## Verifying Your Installation

Run these commands to ensure everything works:

```bash
# 1. Check Python version
python --version

# 2. Verify the CLI is installed
gmail-to-notebooklm --version

# 3. Check installed packages
pip list | grep google-api
pip list | grep beautifulsoup4
pip list | grep html2text

# 4. Test with help command
gmail-to-notebooklm --help
```

## Updating the Tool

To update to the latest version:

```bash
# Pull latest changes (if using git)
git pull origin main

# Reinstall dependencies (in case they changed)
pip install -r requirements.txt

# Reinstall the package
pip install -e .
```

## Uninstalling

To completely remove the tool:

```bash
# Deactivate virtual environment (if active)
deactivate

# Remove virtual environment directory
# On Windows:
rmdir /s .venv
# On macOS/Linux:
rm -rf .venv

# Optionally, remove the entire project directory
```

## Troubleshooting

### "python: command not found"

**Solution**: Python is not installed or not in your PATH.
- Install Python from [python.org](https://www.python.org/)
- On Windows, ensure "Add Python to PATH" is checked during installation

### "pip: command not found"

**Solution**: pip is not installed.
```bash
# Download get-pip.py
python -m ensurepip --upgrade
```

### "No module named google.auth"

**Solution**: Dependencies not installed properly.
```bash
# Ensure virtual environment is activated
# Then reinstall
pip install -r requirements.txt
```

### "gmail-to-notebooklm: command not found"

**Solution**: Package not installed or virtual environment not activated.
```bash
# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate      # Windows

# Install package
pip install -e .
```

### Permission Errors During Installation

**Windows Solution**:
```cmd
# Run Command Prompt as Administrator
```

**macOS/Linux Solution**:
```bash
# Don't use sudo - use a virtual environment instead
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### SSL Certificate Errors

**Solution**: Update certificates.
```bash
pip install --upgrade certifi
```

## Platform-Specific Notes

### Windows

- Use Command Prompt or PowerShell
- PowerShell may require execution policy changes for virtual environment activation:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### macOS

- Python 2.7 comes pre-installed but is deprecated
- Use `python3` and `pip3` explicitly if `python` points to Python 2.7
- You may need to install Xcode Command Line Tools:
  ```bash
  xcode-select --install
  ```

### Linux

- Install Python from your distribution's package manager:
  ```bash
  # Debian/Ubuntu
  sudo apt update
  sudo apt install python3 python3-pip python3-venv

  # Fedora
  sudo dnf install python3 python3-pip

  # Arch
  sudo pacman -S python python-pip
  ```

## Next Steps

- Read [QUICKSTART.md](QUICKSTART.md) for a quick getting started guide
- See [USAGE.md](USAGE.md) for comprehensive usage instructions
- Review [CONFIGURATION.md](CONFIGURATION.md) for configuration options

## Getting Help

If you encounter issues not covered here:
1. Check [OAUTH_SETUP.md](OAUTH_SETUP.md) for authentication issues
2. Review [GitHub Issues](https://github.com/yourusername/gmail-to-notebooklm/issues)
3. Open a new issue with details about your problem
