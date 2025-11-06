# Building the Windows Installer

This guide explains how to build standalone executables and Windows installer for Gmail to NotebookLM.

## Prerequisites

1. **Python 3.9+** with all dependencies installed
2. **PyInstaller** (installed automatically)
3. **Inno Setup 6.0+** (for creating the installer)
   - Download from: https://jrsoftware.org/isinfo.php
   - Install to default location (C:\Program Files (x86)\Inno Setup 6\)

## Quick Build

### Option 1: Build Everything (Executables + Installer)

```bash
# Install dependencies
pip install pyinstaller

# Build both executables
python -m PyInstaller g2n.spec --clean
python -m PyInstaller g2n-gui.spec --clean

# Build installer with Inno Setup
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

The installer will be created in `installer_output\gmail-to-notebooklm-setup-0.3.0.exe`

### Option 2: Build Only Executables

```bash
# CLI executable
python -m PyInstaller g2n.spec --clean

# GUI executable
python -m PyInstaller g2n-gui.spec --clean
```

Executables will be in the `dist\` directory:
- `dist\g2n.exe` - Command-line interface (33MB)
- `dist\g2n-gui.exe` - Desktop GUI (36MB)

## File Structure

```
gmail-to-notebooklm/
├── g2n.spec                 # PyInstaller spec for CLI
├── g2n-gui.spec             # PyInstaller spec for GUI
├── installer.iss            # Inno Setup script
├── dist/                    # Built executables
│   ├── g2n.exe             # Standalone CLI
│   └── g2n-gui.exe         # Standalone GUI
├── build/                   # Build artifacts (temporary)
└── installer_output/        # Final installer
    └── gmail-to-notebooklm-setup-0.3.0.exe
```

## PyInstaller Spec Files

### g2n.spec (CLI)
- **Entry point**: `gmail_to_notebooklm\main.py`
- **Console**: Yes (CLI needs console window)
- **Size**: ~33MB
- **Excludes**: Tkinter/GUI dependencies (not needed for CLI)

### g2n-gui.spec (GUI)
- **Entry point**: `gmail_to_notebooklm\gui\app.py`
- **Console**: No (GUI runs without console window)
- **Size**: ~36MB
- **Includes**: Full Tkinter/GUI support

## Installer Features

The Inno Setup installer (`installer.iss`) provides:

1. **Easy Installation**
   - Standard Windows installer experience
   - Default install location: `C:\Program Files\Gmail to NotebookLM\`
   - Can be installed per-user (no admin rights required)

2. **Optional Features**
   - Desktop shortcut (optional)
   - Add to PATH (allows running `g2n` and `g2n-gui` from any terminal)

3. **Included Files**
   - Both executables (`g2n.exe` and `g2n-gui.exe`)
   - Documentation (README.md, QUICKSTART.md, USAGE.md, OAUTH_SETUP.md)
   - License file

4. **Uninstaller**
   - Clean removal of all files
   - Automatic PATH cleanup if added

## Customization

### Adding an Icon

1. Create or obtain a 256x256 icon file (`app.ico`)
2. Update the spec files:
   ```python
   exe = EXE(
       ...
       icon='app.ico',  # Add this line
   )
   ```
3. Update `installer.iss`:
   ```ini
   SetupIconFile=app.ico
   ```

### Changing Version

Update version in three places:

1. **pyproject.toml**:
   ```toml
   version = "0.4.0"
   ```

2. **installer.iss**:
   ```ini
   #define MyAppVersion "0.4.0"
   ```

3. Rebuild everything

## Testing the Installer

### Test on Clean System

For best results, test the installer on a clean Windows system:

1. Install Windows 11 VM (or use Windows Sandbox)
2. Copy the installer: `gmail-to-notebooklm-setup-0.3.0.exe`
3. Run the installer
4. Test both GUI and CLI:
   ```bash
   g2n-gui            # Should launch GUI
   g2n --help         # Should show CLI help (if added to PATH)
   ```

### What to Test

- [ ] Installer runs without errors
- [ ] Desktop shortcut created (if selected)
- [ ] GUI launches from Start Menu
- [ ] GUI launches from desktop shortcut
- [ ] PATH integration works (if selected)
- [ ] `g2n --help` works from any directory
- [ ] Uninstaller removes all files
- [ ] Uninstaller removes PATH entry

## Troubleshooting

### PyInstaller Errors

**Error**: `ModuleNotFoundError: No module named 'X'`
**Fix**: Add module to `hiddenimports` list in spec file

**Error**: `FileNotFoundError: version_info.txt`
**Fix**: Remove the `version='version_info.txt'` line from spec file (already done)

### Inno Setup Errors

**Error**: `Cannot find file: LICENSE`
**Fix**: Ensure LICENSE file exists in root directory

**Error**: `[Files] Source file not found`
**Fix**: Build executables first using PyInstaller

### Runtime Errors

**Error**: GUI window doesn't appear
**Fix**: Check that `console=False` in `g2n-gui.spec`

**Error**: "Failed to execute script"
**Fix**: Ensure all hidden imports are included in spec file

## Distribution

### Distributing the Installer

The final installer is self-contained and can be distributed directly:
- Upload to GitHub Releases
- Share via cloud storage
- Host on your website

**File**: `installer_output\gmail-to-notebooklm-setup-0.3.0.exe`
**Size**: ~35-40 MB (compressed installer)

### Distributing Portable Executables

You can also distribute the executables without an installer:

1. Create a ZIP file:
   ```
   gmail-to-notebooklm-portable-0.3.0.zip
   ├── g2n.exe
   ├── g2n-gui.exe
   ├── README.md
   └── QUICKSTART.md
   ```

2. Users can extract and run directly (no installation required)

## GitHub Release Example

Create a GitHub release with these artifacts:

```
Gmail to NotebookLM v0.3.0

Downloads:
- gmail-to-notebooklm-setup-0.3.0.exe (Windows Installer)
- gmail-to-notebooklm-portable-0.3.0.zip (Portable)
- Source code (zip)
- Source code (tar.gz)
```

## Automated Builds

For CI/CD pipelines, you can automate the build process:

```yaml
# .github/workflows/build.yml
name: Build Installer

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -e .
          pip install pyinstaller

      - name: Build executables
        run: |
          python -m PyInstaller g2n.spec --clean
          python -m PyInstaller g2n-gui.spec --clean

      - name: Build installer
        run: |
          choco install innosetup -y
          iscc installer.iss

      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: installer
          path: installer_output/*.exe
```

## Next Steps

After building the installer:

1. **Test thoroughly** on clean Windows systems
2. **Create GitHub release** with binaries
3. **Update documentation** with download links
4. **Sign the executables** (optional, requires code signing certificate)
5. **Submit to Microsoft Store** (optional, for wider distribution)

## Support

For build issues:
- Check build logs in `build\g2n\` and `build\g2n-gui\`
- Review warnings in `warn-g2n.txt` and `warn-g2n-gui.txt`
- Open an issue on GitHub with full error messages
