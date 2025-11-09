# Windows Setup Guide

Quick setup guide for Gmail to NotebookLM on Windows.

## Installation

1. **Install the package:**
```bash
pip install -e .
```

2. **Add Scripts to PATH (choose one method):**

### Method A: PowerShell Script (Recommended)
```powershell
# Run the automated setup script
.\setup_path.ps1
```

This script will:
- Add the Scripts directory to your PATH
- Test that commands are working
- Show you available commands

### Method B: Manual Setup
1. Add this directory to your PATH:
   ```
   C:\Users\paul\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\Scripts
   ```

2. Steps:
   - Press `Win + X` and select "System"
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "User variables", select "Path" and click "Edit"
   - Click "New" and paste the Scripts directory path
   - Click "OK" on all dialogs
   - **Restart your terminal**

## Usage

After restarting your terminal, you can use these commands:

### Desktop GUI
```bash
# Full command
gmail-to-notebooklm-gui

# Short alias
g2n-gui
```

### Command Line
```bash
# Full command
gmail-to-notebooklm --label Work --output-dir ./exports

# Short alias
g2n --label Work --output-dir ./exports
```

## Alternative: Run without PATH

If you don't want to modify your PATH, you can run directly:

```bash
# GUI
python -m gmail_to_notebooklm.gui.main

# CLI
python -m gmail_to_notebooklm.main --label Work
```

## Available Command Aliases

| Full Command | Short Alias | Purpose |
|--------------|-------------|---------|
| `gmail-to-notebooklm` | `g2n` | CLI interface |
| `gmail-to-notebooklm-gui` | `g2n-gui` | Desktop GUI |

## Troubleshooting

### Commands not found
- Make sure you restarted your terminal after running setup
- Verify the Scripts directory is in your PATH:
  ```powershell
  $env:Path -split ';' | Select-String "Python313"
  ```

### Permission errors
- Run PowerShell as Administrator if the setup script fails
- Or use Method B (Manual Setup) instead

### GUI doesn't launch
- Try: `python -m gmail_to_notebooklm.gui.main`
- Check if tkinter is installed: `python -c "import tkinter"`

## Next Steps

1. **First time setup:**
   ```bash
   g2n-gui
   ```
   Click "Setup Wizard" to configure OAuth credentials.

2. **CLI usage:**
   ```bash
   # List available labels
   g2n --list-labels

   # Export emails
   g2n --label Work --output-dir ./exports

   # Dry run
   g2n --label Work --dry-run
   ```

3. **Read the documentation:**
   - [QUICKSTART.md](QUICKSTART.md) - 5-minute getting started
   - [USAGE.md](USAGE.md) - Comprehensive usage guide
   - [OAUTH_SETUP.md](OAUTH_SETUP.md) - OAuth credentials setup

## Support

For issues or questions:
- GitHub Issues: https://github.com/pgd1001/gmail-to-notebooklm/issues
- Documentation: See README.md
