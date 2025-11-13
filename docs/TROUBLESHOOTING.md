# Troubleshooting Guide

Having trouble with Gmail to NotebookLM? This guide covers the most common issues and how to fix them.

## Before You Start

**Enable Verbose Output** for more detailed error messages:

```bash
# CLI
g2n --label "Inbox" --verbose

# GUI - Look for "Verbose" checkbox in Settings
```

---

## Quick Diagnosis

### The app won't start

**Windows .exe (GUI)**:
1. Try running as Administrator
2. Check if antivirus is blocking it
3. Ensure Windows is up to date
4. Try redownloading the latest version

**Python/CLI**:
```bash
# Check Python is installed
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Try running directly
python -m gmail_to_notebooklm.main --help
```

**If still stuck**: Go to [Getting Support](#getting-support)

---

## Authentication & Setup Issues

### "Credentials file not found" error

**Cause**: The app can't find your credentials to authenticate with Gmail.

**Solutions** (try in order):

1. **If using Windows .exe**:
   - This should have embedded credentials
   - Try clicking "Setup Wizard" button
   - If that doesn't work, move to option 2

2. **If using Python**:
   - Make sure you completed setup: [ADMIN_SETUP.md](./ADMIN_SETUP.md)
   - Check `credentials.json` exists in your project root
   - Or check `~/.gmail-to-notebooklm/credentials.json`

3. **Try setup wizard**:
   - **GUI**: Click "Setup" button at top
   - **CLI**: Run `g2n --help-setup`

4. **Check file path**:
   ```bash
   # Windows
   type credentials.json

   # Mac/Linux
   cat credentials.json

   # Should show: "installed" or "web" key inside
   ```

---

### "Invalid credentials" error

**Cause**: The credentials.json file is corrupted or invalid.

**Solutions**:

1. **Verify file format** - Check it's valid JSON:
   ```bash
   # Should not show errors
   python -m json.tool credentials.json
   ```

2. **Check file contents** - Should have:
   ```json
   {
     "installed": {
       "client_id": "...",
       "client_secret": "...",
       ...
     }
   }
   ```

3. **Redownload credentials**:
   - Delete the corrupted file
   - Follow [ADMIN_SETUP.md](./ADMIN_SETUP.md) to get new credentials

4. **Verify Google Cloud setup**:
   - Login to [Google Cloud Console](https://console.cloud.google.com)
   - Check project exists
   - Check Gmail API is enabled
   - Check OAuth credentials exist

---

### "Unverified app" warning during authentication

**What it is**: Google shows this warning for apps still in testing mode.

**It's normal!** This is expected for the beta version.

**How to proceed**:
1. At the warning screen, click **"Advanced"** (bottom-left)
2. Click **"Go to Gmail to NotebookLM (unsafe)"**
3. Click **"Allow"** to grant read-only Gmail access

**More details**: See [BETA_ACCESS.md](./BETA_ACCESS.md)

---

### "Token expired" error (After 7 days)

**Cause**: In beta mode, Gmail tokens expire after 7 days.

**Solution**:
- **GUI**: Click "Setup Wizard" → Re-authenticate
- **CLI**: Delete `~/.gmail-to-notebooklm/tokens.pickle` then run command again

**Note**: After Google OAuth verification (Q1 2025), tokens will last longer.

---

### Authentication window doesn't open

**Cause**: Browser integration issue or firewall blocking.

**Solutions**:

1. **Check browser is default**:
   - Set your default browser in System Settings
   - Ensure at least one browser is installed

2. **Check firewall**:
   - Disable firewall temporarily to test
   - Add app to firewall whitelist if needed

3. **Manual authentication**:
   ```bash
   # CLI: Copy the URL from error message and paste in browser manually
   # Your browser should show an error about "invalid_grant"
   # That's normal - just authorize the app
   ```

4. **Try different browser**:
   - If default browser isn't working, try another
   - Edge, Chrome, Firefox usually work

---

## Export & File Issues

### "No emails found" despite having emails

**Cause**: Your filter (label, query, date range) excluded all emails.

**Solutions**:

1. **Check label name**:
   ```bash
   # List all available labels
   g2n --list-labels

   # Try exact name from list
   g2n --label "Exact Name From List"
   ```

2. **Check query/filters**:
   ```bash
   # Try without filters first
   g2n --label "Inbox"

   # If that works, add filters one at a time
   g2n --label "Inbox" --after "2024-01-01"
   g2n --label "Inbox" --from "sender@example.com"
   ```

3. **Try dry-run to see what would export**:
   ```bash
   g2n --label "Inbox" --dry-run --verbose
   ```

4. **Check label has emails**:
   - Open Gmail directly
   - Navigate to the label
   - Make sure emails exist

---

### Files aren't being created

**Cause**: Output directory doesn't exist or no permission to write.

**Solutions**:

1. **Create output directory**:
   ```bash
   # Windows
   mkdir C:\Users\YourName\Documents\gmail-exports

   # Mac/Linux
   mkdir ~/gmail-exports
   ```

2. **Check you have write permission**:
   ```bash
   # Try creating test file
   touch ~/gmail-exports/test.txt
   rm ~/gmail-exports/test.txt

   # If error, fix permissions
   chmod 755 ~/gmail-exports
   ```

3. **Use full path (not relative)**:
   ```bash
   # Instead of: ./output
   # Use: /full/path/to/output
   # Or: C:\Users\YourName\Documents\output
   ```

4. **Check disk space**:
   ```bash
   # Make sure you have enough space
   df -h  # Mac/Linux
   dir C:  # Windows
   ```

---

### "Permission denied" errors

**Cause**: File system permissions issue.

**Solutions**:

1. **Windows**:
   - Right-click app → Run as Administrator
   - Check file isn't marked read-only
   - Disable antivirus temporarily to test

2. **Mac/Linux**:
   ```bash
   # Make directory writable
   chmod 755 ~/gmail-exports

   # Make files writable
   chmod 644 ~/gmail-exports/*
   ```

3. **Check antivirus**:
   - Disable temporarily to test
   - Add app to antivirus whitelist

---

### Markdown files are empty or have strange characters

**Cause**: HTML parsing or encoding issue.

**Solutions**:

1. **Check email has content**:
   - Open the email in Gmail
   - Make sure it has a body (not just attachments)

2. **Verify file encoding**:
   - Files should be UTF-8
   - Try opening in VS Code or Sublime (they handle UTF-8 better)

3. **Check for special content**:
   - Some emails have complex HTML/CSS
   - The app converts best effort - some styling may be lost
   - Content should always be readable

4. **Try re-exporting**:
   ```bash
   # Delete old files and re-export
   rm ~/gmail-exports/*.md
   g2n --label "Inbox" --max-results 5 --verbose
   ```

---

## GUI-Specific Issues

### Buttons don't respond

**Cause**: App might be loading or processing.

**Solutions**:

1. **Wait for processing**:
   - Check progress dialog (might be behind main window)
   - Look for progress bar or status messages

2. **Force quit and restart**:
   - Press Ctrl+C in console (if running from Python)
   - Or force quit application
   - Restart and try again

3. **Check for dialogs**:
   - There might be a dialog window behind main window
   - Alt+Tab to see all windows
   - Look for dialog boxes

---

### Settings aren't saving

**Cause**: File permission or config file issue.

**Solutions**:

1. **Check file permissions**:
   ```bash
   # Windows
   dir %APPDATA%\gmail_to_notebooklm

   # Mac
   ls -la ~/.gmail-to-notebooklm/

   # Linux
   ls -la ~/.gmail-to-notebooklm/
   ```

2. **Recreate config directory**:
   ```bash
   # Backup first!
   cp -r ~/.gmail-to-notebooklm ~/.gmail-to-notebooklm.backup

   # Delete and recreate
   rm -rf ~/.gmail-to-notebooklm
   # Run app to auto-create
   ```

3. **Check for locked files**:
   - Make sure no other instance is running
   - Close app completely
   - Try again

---

### GUI freezes during export

**Cause**: Large export taking time (app is working, not frozen).

**Solutions**:

1. **Wait longer**:
   - Large exports can take minutes
   - Watch the progress dialog for activity
   - Don't force quit

2. **Use smaller export**:
   ```bash
   # Try with limit first
   g2n --max-results 10

   # Once that works, increase gradually
   g2n --max-results 50
   g2n --max-results 100
   ```

3. **Check system resources**:
   - Close other apps
   - Ensure you have RAM available
   - Check disk isn't full

4. **If truly frozen** (progress stops for 5+ min):
   - Force quit app
   - Check for errors in the verbose output
   - Report issue with details

---

## CLI-Specific Issues

### "Command not found: g2n"

**Cause**: Command not in PATH or not installed.

**Solutions**:

1. **Install the package**:
   ```bash
   pip install -e .
   ```

2. **Use Python module form**:
   ```bash
   # Instead of g2n --label "Inbox"
   python -m gmail_to_notebooklm.main --label "Inbox"
   ```

3. **Check installation**:
   ```bash
   # Should show installed
   pip show gmail-to-notebooklm
   ```

4. **Check PATH**:
   ```bash
   # Linux/Mac - Check if pip install location in PATH
   which g2n

   # Windows - g2n should be in Python Scripts folder
   where g2n
   ```

---

### Script output is garbled or shows nothing

**Cause**: Terminal encoding or output issue.

**Solutions**:

1. **Use quiet mode** (simpler output):
   ```bash
   g2n --label "Inbox" --quiet
   ```

2. **Set UTF-8 encoding**:
   ```bash
   # Windows PowerShell
   [Console]::OutputEncoding = [System.Text.Encoding]::UTF8

   # Linux/Mac
   export LANG=en_US.UTF-8
   ```

3. **Use JSON output**:
   ```bash
   g2n --label "Inbox" --json-output

   # Pipe to file
   g2n --label "Inbox" --json-output > results.json
   ```

---

### "Rate limit exceeded" error

**Cause**: Gmail API has limits on requests.

**Solutions**:

1. **Wait and retry**:
   - Gmail limits are per-user
   - Usually reset within an hour
   - Try again later

2. **Use smaller batches**:
   ```bash
   # Instead of --max-results 1000
   g2n --max-results 100  # Smaller batches
   ```

3. **Space out exports**:
   - Wait between large exports
   - Don't run multiple exports simultaneously

---

## Performance Issues

### Export is very slow

**Cause**: Normal for large exports; network/system dependent.

**What's normal**:
- 10 emails: ~10-30 seconds
- 100 emails: ~1-3 minutes
- 1000 emails: ~10-30 minutes

**To speed up**:

1. **Use filters**:
   ```bash
   # Instead of all emails, filter first
   g2n --label "Inbox" --after "2024-01-01"  # Recent only
   ```

2. **Increase batch size**:
   ```bash
   # Default handles ~50 emails at a time
   # Gmail API limit is 100
   # This is usually optimal
   ```

3. **Check network**:
   - Slow internet = slow export
   - WiFi can be slower than wired
   - Try wired if available

4. **Check system**:
   - Close other apps
   - Check disk isn't full
   - Ensure you have RAM available

---

## System-Specific Issues

### Windows Issues

**App won't launch from Start Menu**:
1. Check app is installed to Program Files
2. Try running from command line instead
3. Reinstall if corrupted

**Antivirus warnings**:
- This is normal for unsigned executables
- The app is safe - it's open source and auditable
- Add to antivirus whitelist if needed

**Path issues**:
```bash
# Windows PowerShell might show errors
# Try Command Prompt (cmd.exe) instead
```

### Mac Issues

**"Cannot be opened because the developer cannot be verified"**:
1. Right-click the app
2. Click "Open"
3. Click "Open" in dialog

**Or use CLI instead**:
```bash
brew install python
pip install gmail-to-notebooklm
g2n --help
```

### Linux Issues

**Tkinter not installed** (for GUI):
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

---

## Advanced Troubleshooting

### Enable Debug Logging

**CLI**:
```bash
# Maximum verbosity
g2n --label "Inbox" --verbose

# Save to file for analysis
g2n --label "Inbox" --verbose > debug.log 2>&1
```

**Python**:
```python
# Enable debug logging in code
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Log Files

**Default locations**:
```bash
# Windows
%APPDATA%\gmail_to_notebooklm\debug.log
C:\Users\YourName\AppData\Roaming\gmail_to_notebooklm

# Mac/Linux
~/.gmail-to-notebooklm/debug.log
~/.gmail-to-notebooklm/
```

### Verify API Access

```bash
# Test Gmail API connectivity
python -c "from gmail_to_notebooklm.gmail_client import GmailClient; gc = GmailClient('creds'); print(gc.list_labels())"

# Test OAuth
python -c "from gmail_to_notebooklm.auth import authenticate; auth = authenticate(); print('Success' if auth else 'Failed')"
```

### Reset Everything

**WARNING**: This removes all saved settings!

```bash
# Backup first
cp -r ~/.gmail-to-notebooklm ~/.gmail-to-notebooklm.backup

# Remove all config/data
rm -rf ~/.gmail-to-notebooklm

# Remove tokens
rm -rf ~/.gmail-to-notebooklm/tokens.pickle

# Restart app - will recreate fresh
```

---

## Still Having Issues?

### Getting Support

1. **Check this guide** - Search for your error message
2. **Check GETTING_HELP.md** - Links to other docs
3. **Check GitHub Issues** - Similar issues might be solved
4. **Open a new issue** - Include details from below

### When Opening an Issue

**Include these details**:

```
**Title**: Clear, short description of problem

**What I did**:
1. Clicked X
2. Entered Y
3. Got error Z

**Error message** (exact text):
[Paste full error message here]

**Environment**:
- OS: Windows 11 / Mac / Linux
- Version: 0.3.0 (from Help → About)
- Python: 3.9 / 3.10 / 3.11 (if applicable)
- Installation: .exe / Python package

**What I expected**:
[Describe what should happen]

**What happened instead**:
[Describe what actually happened]

**Steps to reproduce**:
[Clear step-by-step instructions]

**Additional context**:
[Any other helpful info]
```

### Useful Information to Gather

```bash
# System info
python --version
pip show gmail-to-notebooklm
g2n --version

# Verbose output from failed command
g2n --label "Inbox" --verbose 2>&1 | tee error_log.txt

# List of labels (sanitize email addresses)
g2n --list-labels
```

---

## Common Solutions Checklist

Before posting an issue, try:

- [ ] Restart the app
- [ ] Check internet connection
- [ ] Run `--verbose` to get detailed output
- [ ] Check you're using the latest version
- [ ] Try the command from different directory
- [ ] Clear credentials and redo setup
- [ ] Check Gmail account isn't locked
- [ ] Verify credentials.json is valid JSON
- [ ] Ensure output directory exists and is writable
- [ ] Check disk has free space
- [ ] Disable antivirus temporarily
- [ ] Try running as Administrator (Windows)

---

## Report a Security Issue

**If you find a security vulnerability**, please email:
[your.email@example.com]

Do NOT open a public issue for security vulnerabilities.

---

**Last Updated**: November 2025
**Version**: 1.0

Still stuck? Open an issue at: [GitHub Issues](https://github.com/yourusername/gmail-to-notebooklm/issues)
