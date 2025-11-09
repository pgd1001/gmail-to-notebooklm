# Distribution Guide

This document explains how to distribute Gmail to NotebookLM to end users.

## Distribution Methods

There are three primary ways to distribute this application:

### 1. Windows Installer (Recommended)

**Best for**: Most users who want a traditional installation experience

**File**: `gmail-to-notebooklm-setup-0.3.0.exe`
**Size**: ~35-40 MB

**Features**:
- One-click installation
- Start menu integration
- Optional desktop shortcut
- Optional PATH integration
- Clean uninstaller
- No Python required

**How to Create**:
```bash
# Build executables
python -m PyInstaller g2n.spec --clean
python -m PyInstaller g2n-gui.spec --clean

# Build installer (requires Inno Setup)
iscc installer.iss
```

**Distribution**:
- Upload to GitHub Releases
- Host on your website
- Share via cloud storage (Google Drive, Dropbox, etc.)

### 2. Portable Executables

**Best for**: Users who don't want to install, IT admins, USB drives

**Files**:
- `g2n.exe` (33 MB)
- `g2n-gui.exe` (36 MB)

**Features**:
- No installation required
- Run from any folder
- Can be placed on USB drive
- No registry changes
- No Python required

**How to Create**:
```bash
# Build executables
python -m PyInstaller g2n.spec --clean
python -m PyInstaller g2n-gui.spec --clean

# Create portable package
zip -r gmail-to-notebooklm-portable-0.3.0.zip dist/*.exe README.md QUICKSTART.md
```

**Distribution**:
- Package as ZIP file
- Include README and QUICKSTART
- Upload to GitHub Releases

### 3. Python Package (pip)

**Best for**: Developers, Python users, automation

**Installation**:
```bash
pip install gmail-to-notebooklm
```

**Features**:
- Smallest download size
- Easy updates (`pip install --upgrade`)
- Requires Python 3.9+
- Access to source code
- Can be imported as library

**How to Publish**:
```bash
# Build package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

## GitHub Releases

### Creating a Release

1. **Tag the version**:
   ```bash
   git tag v0.3.0
   git push origin v0.3.0
   ```

2. **Build all artifacts**:
   ```bash
   # Windows installer
   python -m PyInstaller g2n.spec --clean
   python -m PyInstaller g2n-gui.spec --clean
   iscc installer.iss

   # Portable ZIP
   cd dist
   zip -r ../gmail-to-notebooklm-portable-0.3.0.zip g2n.exe g2n-gui.exe ../README.md ../QUICKSTART.md
   cd ..
   ```

3. **Create GitHub release**:
   - Go to: https://github.com/yourusername/gmail-to-notebooklm/releases
   - Click "Draft a new release"
   - Choose tag: v0.3.0
   - Title: "Gmail to NotebookLM v0.3.0"
   - Description: See template below
   - Upload files:
     - `installer_output/gmail-to-notebooklm-setup-0.3.0.exe`
     - `gmail-to-notebooklm-portable-0.3.0.zip`

### Release Notes Template

```markdown
# Gmail to NotebookLM v0.3.0

## What's New

- Desktop GUI with modern interface
- Enhanced CLI with DevOps features (--dry-run, --json-output, --quiet)
- Export history tracking with SQLite
- Profile management for saved configurations
- Progress bars and rich terminal output
- Short command aliases (g2n, g2n-gui)

## Downloads

### For Windows Users

**Recommended**: [gmail-to-notebooklm-setup-0.3.0.exe](link) (35 MB)
- Traditional Windows installer
- Includes both CLI and GUI
- Optional PATH integration
- No Python required

**Portable**: [gmail-to-notebooklm-portable-0.3.0.zip](link) (70 MB)
- No installation required
- Extract and run
- Can be used from USB drive

### For Python Users

```bash
pip install gmail-to-notebooklm
```

## Installation

### Windows Installer

1. Download `gmail-to-notebooklm-setup-0.3.0.exe`
2. Double-click to run installer
3. Follow the installation wizard
4. Launch from Start Menu or desktop shortcut

### Portable

1. Download `gmail-to-notebooklm-portable-0.3.0.zip`
2. Extract to any folder
3. Run `g2n-gui.exe` for GUI or `g2n.exe` for CLI

## First Run

After installation:

1. **Setup OAuth credentials**: Run the Setup Wizard (GUI) or see [OAUTH_SETUP.md](link)
2. **Export emails**:
   - GUI: Click "Quick Export" or use filters
   - CLI: `g2n --label Work --output-dir ./exports`

## Documentation

- [Quickstart Guide](QUICKSTART.md) - Get started in 5 minutes
- [Usage Guide](USAGE.md) - Comprehensive feature documentation
- [OAuth Setup](OAUTH_SETUP.md) - Setting up Gmail API credentials
- [Windows Setup](SETUP_WINDOWS.md) - Windows-specific instructions

## System Requirements

- **OS**: Windows 10/11 (64-bit)
- **RAM**: 200 MB minimum
- **Disk**: 100 MB for installation + space for exported emails
- **Internet**: Required for Gmail API access

## Changelog

See [CHANGELOG.md](link) for full changelog.

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/gmail-to-notebooklm/issues)
- **Documentation**: [README.md](README.md)
- **Email**: your.email@example.com
```

## Distribution Checklist

Before distributing a new version:

- [ ] Update version in `pyproject.toml`
- [ ] Update version in `installer.iss`
- [ ] Update CHANGELOG.md
- [ ] Test on clean Windows system
- [ ] Build and test CLI executable
- [ ] Build and test GUI executable
- [ ] Build and test installer
- [ ] Create portable ZIP
- [ ] Tag release in Git
- [ ] Create GitHub release
- [ ] Upload all artifacts
- [ ] Update documentation links
- [ ] Publish to PyPI (optional)
- [ ] Announce on social media (optional)

## File Sizes Reference

- **CLI executable**: ~33 MB
- **GUI executable**: ~36 MB
- **Installer (compressed)**: ~35-40 MB
- **Portable ZIP**: ~70 MB
- **Python wheel**: ~50 KB (requires pip install dependencies)

## Security Considerations

### Code Signing

For professional distribution, consider code signing:

1. **Purchase certificate**: From DigiCert, Sectigo, etc.
2. **Sign executables**:
   ```bash
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com g2n.exe
   signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com g2n-gui.exe
   ```
3. **Sign installer**:
   ```ini
   ; Add to installer.iss
   SignTool=signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com $f
   ```

**Benefits**:
- Windows SmartScreen won't warn users
- Shows your organization name
- Users trust signed software more

### Antivirus False Positives

PyInstaller executables sometimes trigger false positives:

1. **Submit to antivirus vendors**: VirusTotal, Microsoft, etc.
2. **Use reputable hosting**: GitHub Releases preferred
3. **Provide checksums**:
   ```bash
   sha256sum g2n.exe > checksums.txt
   sha256sum g2n-gui.exe >> checksums.txt
   sha256sum gmail-to-notebooklm-setup-0.3.0.exe >> checksums.txt
   ```

## Microsoft Store Distribution

For wider distribution, consider Microsoft Store:

1. **Register**: Microsoft Partner Center account ($19 one-time fee)
2. **Package app**: Use MSIX instead of Inno Setup
3. **Submit**: Through Partner Center
4. **Benefits**:
   - Automatic updates
   - Easier discovery
   - Built-in payment (if charging)
   - Digital signature included

## Alternative Distribution Channels

### Chocolatey (Package Manager)

Create a Chocolatey package for easy installation:

```bash
choco install gmail-to-notebooklm
```

### Scoop (Package Manager)

Add to Scoop bucket:

```bash
scoop install gmail-to-notebooklm
```

### Winget (Windows Package Manager)

Submit to winget-pkgs repository:

```bash
winget install gmail-to-notebooklm
```

## Support After Distribution

### Common User Questions

1. **"Python is required?"** - No, the installer/portable versions are standalone
2. **"Is it safe?"** - Yes, open source, can review code
3. **"How to update?"** - Download new version, install over old
4. **"Where are my credentials stored?"** - In `credentials.json` and `token.json` in installation directory

### Analytics (Optional)

Consider adding telemetry to understand usage:

```python
# Optional: Anonymous usage statistics
import requests

def send_analytics(event: str):
    try:
        requests.post('https://analytics.example.com/event', {
            'event': event,
            'version': '0.3.0',
            'platform': 'windows'
        }, timeout=1)
    except:
        pass  # Never let analytics break the app
```

## License Compliance

Ensure you comply with all dependency licenses:

```bash
pip-licenses --format=markdown > THIRD_PARTY_LICENSES.md
```

Include in documentation:
- Your license (MIT in this case)
- Third-party licenses
- Attribution requirements

## Versioning Strategy

Follow Semantic Versioning (SemVer):

- **Major** (1.0.0): Breaking changes
- **Minor** (0.3.0): New features, backwards compatible
- **Patch** (0.3.1): Bug fixes only

Example:
- 0.1.0: Initial release (Phase 1)
- 0.2.0: Added CLI features (Phase 2)
- 0.3.0: Added GUI (Phase 3)
- 0.4.0: Distribution & Packaging (Phase 4)
- 1.0.0: Stable release

## Success Metrics

Track these metrics to measure success:

- Download count (GitHub releases)
- GitHub stars/forks
- Issue count and resolution time
- User feedback/testimonials
- PyPI download statistics

## Next Steps

After completing Phase 4 distribution:

1. **Monitor feedback**: Watch GitHub issues
2. **Fix bugs**: Release patch versions as needed
3. **Plan Phase 5**: Cloud features, advanced functionality
4. **Build community**: Encourage contributions
5. **Document well**: Keep docs up to date
