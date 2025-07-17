# this_file: phiton.spec
# 
# PyInstaller spec file for Phiton
# Builds a single executable file with all dependencies

# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

block_cipher = None

a = Analysis(
    ['src/phiton/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/phiton', 'phiton'),
    ],
    hiddenimports=[
        'phiton.cli',
        'phiton.config',
        'phiton.constants',
        'phiton.dephitonize',
        'phiton.phitonize',
        'phiton.utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'jupyter',
        'IPython',
        'notebook',
        'scipy',
        'sklearn',
        'tensorflow',
        'torch',
        'cv2',
        'PIL',
        'Pillow',
    ],
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
    name='phiton',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)