# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for Gmail to NotebookLM GUI (g2n-gui.exe)"""

from PyInstaller.utils.hooks import collect_data_files, collect_submodules
import os

block_cipher = None

# Collect all Google API client modules + GUI modules
hiddenimports = [
    'googleapiclient.discovery',
    'googleapiclient.http',
    'google.auth.transport.requests',
    'google_auth_oauthlib.flow',
    'google_auth_httplib2',
    'click',
    'rich.console',
    'rich.progress',
    'rich.table',
    'bs4',
    'lxml.etree',
    'html2text',
    'yaml',
    'dateutil.parser',
    'tkinter',
    'tkinter.ttk',
    'tkinter.simpledialog',
    'tkinter.messagebox',
    'tkinter.filedialog',
    'gmail_to_notebooklm.gui.app',
    'gmail_to_notebooklm.gui.main',
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
    excludes=['matplotlib', 'numpy', 'pandas', 'scipy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=True,
    optimize=2,  # Optimize Python bytecode (remove docstrings, line numbers, etc.)
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
    strip=False,  # Disable strip - not available on Windows Microsoft Store Python
    upx=False,
    runtime_tmpdir=None,
    console=False,  # GUI should not show console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
