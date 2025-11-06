# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for Gmail to NotebookLM GUI (g2n-gui.exe)"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

block_cipher = None

# Collect all Google API client modules + GUI modules
hiddenimports = [
    'googleapiclient',
    'googleapiclient.discovery',
    'googleapiclient.http',
    'google.auth',
    'google.auth.transport',
    'google.auth.transport.requests',
    'google_auth_oauthlib',
    'google_auth_oauthlib.flow',
    'google_auth_httplib2',
    'httplib2',
    'oauth2client',
    'click',
    'rich',
    'rich.console',
    'rich.progress',
    'rich.table',
    'beautifulsoup4',
    'bs4',
    'lxml',
    'lxml.etree',
    'html2text',
    'yaml',
    'dateutil',
    'dateutil.parser',
    'tkinter',
    'tkinter.ttk',
    'tkinter.simpledialog',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'gmail_to_notebooklm',
    'gmail_to_notebooklm.gui',
    'gmail_to_notebooklm.gui.app',
    'gmail_to_notebooklm.gui.main',
    'gmail_to_notebooklm.gui.windows',
    'gmail_to_notebooklm.gui.windows.main_window',
    'gmail_to_notebooklm.gui.windows.settings_dialog',
    'gmail_to_notebooklm.gui.windows.oauth_wizard',
    'gmail_to_notebooklm.gui.windows.export_dialog',
    'gmail_to_notebooklm.gui.windows.history_dialog',
    'gmail_to_notebooklm.gui.windows.profiles_dialog',
    'gmail_to_notebooklm.main',
    'gmail_to_notebooklm.config',
    'gmail_to_notebooklm.auth',
    'gmail_to_notebooklm.gmail_client',
    'gmail_to_notebooklm.parser',
    'gmail_to_notebooklm.converter',
    'gmail_to_notebooklm.utils',
    'gmail_to_notebooklm.core',
    'gmail_to_notebooklm.history',
    'gmail_to_notebooklm.profiles',
]

# Collect data files
datas = [
    ('gmail_to_notebooklm/data', 'gmail_to_notebooklm/data'),  # Include data directory with embedded credentials
]

a = Analysis(
    ['gmail_to_notebooklm\\gui\\app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='g2n-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI should not show console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
