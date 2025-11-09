# Simplified Setup Guide

**For users of the pre-built Windows executable**

This guide is for users who downloaded the standalone Windows installer or portable executables. No Python installation or Google Cloud Console setup required!

## Prerequisites

- Windows 10 or 11 (64-bit)
- Gmail account
- Internet connection

That's it! No Python, no Google Cloud Project needed.

## Installation

### Option 1: Windows Installer (Recommended)

1. Download `gmail-to-notebooklm-setup-0.4.0.exe` from [GitHub Releases](https://github.com/pgd1001/gmail-to-notebooklm/releases)

2. Run the installer:
   - Double-click the downloaded file
   - Follow the installation wizard
   - Optional: Add desktop shortcut
   - Optional: Add to PATH for command-line access

3. Launch the application:
   - From Start Menu: Search for "Gmail to NotebookLM"
   - From Desktop: Double-click shortcut (if created)
   - From Command Line: `g2n-gui` (if added to PATH)

### Option 2: Portable Executable

1. Download `gmail-to-notebooklm-portable-0.4.0.zip` from [GitHub Releases](https://github.com/pgd1001/gmail-to-notebooklm/releases)

2. Extract the ZIP file to any folder

3. Run the application:
   - For GUI: Double-click `g2n-gui.exe`
   - For CLI: Open terminal, run `g2n.exe --help`

## First Run: Authentication

### Desktop GUI

1. Launch the application (`g2n-gui.exe` or from Start Menu)

2. Click **"Setup Wizard"** button

3. When prompted, click **"Authenticate with Gmail"**

4. A browser window will open automatically

5. Sign in to your Gmail account

6. Review permissions:
   - Read-only access to Gmail
   - No ability to send or delete emails

7. Click **"Allow"**

8. You'll see "Authentication successful!" - close the browser

9. Return to the application - you're ready to export!

### Command Line

1. Open terminal (Command Prompt or PowerShell)

2. Navigate to the folder containing `g2n.exe` (or use it from PATH)

3. Run your first export:
   ```bash
   g2n --label INBOX --output-dir ./my-exports
   ```

4. A browser window will open automatically

5. Sign in to Gmail and click "Allow"

6. The export will begin automatically

## Common First-Time Questions

### "Is this safe?"

Yes! The application:
- ✅ Uses official Google OAuth 2.0 authentication
- ✅ Has **read-only** access to your Gmail (cannot send or delete emails)
- ✅ Stores authentication tokens locally on your computer only
- ✅ Never sends your data to any third-party servers
- ✅ Is open-source - you can review the code

### "Why does it say 'unverified app'?"

The application is currently in Testing mode with Google, which means:
- Limited to 100 beta users
- Shows "unverified app" warning during first login
- Completely safe to continue - just click "Advanced" then "Go to Gmail to NotebookLM (unsafe)"

This is normal for applications that haven't completed Google's verification process yet. The application is safe and only requests read-only Gmail access.

### "Do I need a Google Cloud Project?"

**No!** That's the whole point of this simplified setup. The application includes embedded OAuth credentials, so you can authenticate directly without any Google Cloud Console setup.

Advanced users who want more control can create their own credentials (see [ADVANCED_SETUP.md](ADVANCED_SETUP.md)).

### "Where are my Gmail credentials stored?"

The application stores:
- **OAuth tokens**: In `token.json` in your user directory
- **No passwords**: The app never sees your Gmail password
- **Read-only access**: Cannot send, delete, or modify emails

You can revoke access anytime from: https://myaccount.google.com/permissions

### "Does this work offline?"

Initial authentication requires internet connection. After authentication, the app needs internet to access Gmail and download emails, but the conversion to Markdown happens locally.

### "How do I update to a new version?"

**Installer version:**
- Download the new installer
- Run it - it will upgrade the existing installation

**Portable version:**
- Download the new ZIP
- Extract to replace old files
- Your tokens and settings are preserved

## Using the Desktop GUI

### Quick Export

1. Launch the GUI

2. Select options:
   - **Label**: Choose a Gmail label (e.g., "Work", "INBOX")
   - **Output Directory**: Where to save Markdown files
   - **Options**: Date organization, index creation, etc.

3. Click **"Start Export"**

4. Wait for progress bar to complete

5. Click **"Open Output Directory"** to view your exported emails

### Advanced Features

**Export Profiles**:
- Save commonly used configurations
- Click "Profiles" to manage saved settings
- Load profiles for quick exports

**Export History**:
- View past exports with statistics
- Click "History" to see all previous exports
- Re-export with same settings

**Settings**:
- Configure default output directory
- Adjust credential paths (advanced)
- Customize export preferences

## Using the Command Line

### Basic Commands

```bash
# Export a specific label
g2n --label Work --output-dir ./exports

# Export with date range
g2n --label INBOX --after 2024-01-01 --before 2024-12-31

# Export with Gmail query
g2n --query "is:unread from:boss@company.com"

# Organize by date with index
g2n --label Projects --organize-by-date --create-index

# Dry run (see what would be exported)
g2n --label INBOX --dry-run

# List all available labels
g2n --list-labels
```

### Command Reference

```bash
g2n --help                    # Show all options
g2n --version                 # Show version
g2n --list-labels             # List Gmail labels
g2n --label NAME              # Export specific label
g2n --query "SEARCH"          # Use Gmail search syntax
g2n --after DATE              # Filter by start date
g2n --before DATE             # Filter by end date
g2n --from EMAIL              # Filter by sender
g2n --to EMAIL                # Filter by recipient
g2n --output-dir PATH         # Set output directory
g2n --organize-by-date        # Organize into date folders
g2n --create-index            # Generate INDEX.md
g2n --dry-run                 # Preview without exporting
g2n --quiet                   # Minimal output
g2n --json-output             # JSON format output
```

## Troubleshooting

### "Browser doesn't open for authentication"

1. **Manual URL**: The terminal will show a URL - copy and paste it into your browser
2. **Firewall**: Check if firewall is blocking the local OAuth server
3. **Port conflict**: The app uses a random port, try again

### "Authentication failed"

1. **Browser**: Make sure you completed the authentication in the browser
2. **Token**: Try deleting `token.json` and re-authenticating
3. **Credentials**: If you see "credentials not found", the embedded credentials may be missing

### "Unverified app warning"

This is normal for apps in Testing mode. To continue:

1. Click **"Advanced"** at the bottom of the warning
2. Click **"Go to Gmail to NotebookLM (unsafe)"**
3. Review permissions and click **"Allow"**

The app is safe - it only requests read-only Gmail access.

### "No labels found"

1. Make sure you completed authentication
2. Check that your Gmail account has labels
3. Try running: `g2n --list-labels` to see available labels

### "Permission denied" errors

1. **Output directory**: Make sure you have write permissions
2. **Antivirus**: Some antivirus software may block the .exe - add an exception
3. **Windows SmartScreen**: Click "More info" then "Run anyway"

### "The app won't start"

1. **Windows version**: Requires Windows 10 or 11 (64-bit)
2. **Antivirus**: Check if antivirus is blocking the exe
3. **Dependencies**: The .exe is standalone - no dependencies needed
4. **Logs**: Check the console output for error messages

## Getting Help

### Documentation

- **This guide**: Simplified setup (current file)
- **[QUICKSTART.md](QUICKSTART.md)**: 5-minute getting started
- **[USAGE.md](USAGE.md)**: Comprehensive feature documentation
- **[ADVANCED_SETUP.md](ADVANCED_SETUP.md)**: Create your own OAuth credentials

### Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/pgd1001/gmail-to-notebooklm/issues)
- **Email**: pgd1001@gmail.com
- **Documentation**: Full docs at [README.md](README.md)

### Beta Testing Program

This application is currently in **Testing mode** with Google, which means it's limited to 100 beta users.

**Want to become a beta tester?**

See [BETA_ACCESS.md](BETA_ACCESS.md) for instructions on requesting access.

**When will it be fully verified?**

We plan to complete Google's verification process when we have:
- Sufficient beta testing feedback
- Polished user experience
- Complete documentation
- Privacy policy published

After verification:
- ✅ No more "unverified app" warnings
- ✅ No user limits
- ✅ Longer-lasting authentication tokens
- ✅ Professional verified status

## Next Steps

Now that you're set up, explore the features:

1. **Try different exports**: Labels, date ranges, queries
2. **Organize exports**: Use date-based organization and index files
3. **Upload to NotebookLM**: Use exported Markdown files as knowledge sources
4. **Save profiles**: Save your common export configurations
5. **View history**: Track your exports over time

## Privacy & Security

### What data does the app access?

- ✅ **Gmail messages**: Read-only access to download emails
- ❌ **No sending**: Cannot send emails
- ❌ **No deleting**: Cannot delete or modify emails
- ❌ **No contacts**: Does not access your contacts
- ❌ **No calendar**: Does not access calendar

### Where is data stored?

- **Exported emails**: Locally in your chosen output directory (Markdown files)
- **Authentication tokens**: Locally in `token.json` (your computer only)
- **Settings**: Locally in config files (your computer only)
- **No cloud storage**: Nothing is sent to external servers

### How to revoke access?

1. Go to: https://myaccount.google.com/permissions
2. Find "Gmail to NotebookLM"
3. Click "Remove Access"

You can re-authenticate anytime by running the app again.

## Advanced Topics

### Using Your Own Credentials

If you want more control, you can create your own Google Cloud Project and credentials:

1. See [ADVANCED_SETUP.md](ADVANCED_SETUP.md) for detailed instructions
2. Place your `credentials.json` in the same directory as the .exe
3. The app will use your credentials instead of the embedded ones

### Command Line Power Users

```bash
# Add g2n to your PATH for easy access
# (Installer can do this automatically)

# Then use it from anywhere:
g2n --label Work --output-dir C:\Exports\Work
g2n --query "is:unread newer_than:7d" --output-dir C:\Exports\Recent

# Use in scripts:
g2n --label Work --json-output > export-results.json

# Automated exports:
g2n --label Daily --quiet --output-dir C:\Exports\Daily
```

### Portable USB Drive Use

The portable .exe files can run from a USB drive:

1. Extract `g2n.exe` and `g2n-gui.exe` to USB drive
2. Run directly from the USB drive
3. Authentication tokens are stored relative to the exe location
4. Perfect for using on multiple computers

## Feedback

We'd love to hear from you!

- **Found a bug?** [Open an issue](https://github.com/pgd1001/gmail-to-notebooklm/issues)
- **Have a suggestion?** [Open an issue](https://github.com/pgd1001/gmail-to-notebooklm/issues)
- **Love the app?** Leave a ⭐ on [GitHub](https://github.com/pgd1001/gmail-to-notebooklm)

---

**Version**: 0.4.0
**Last Updated**: 2025-11-06
**License**: MIT
