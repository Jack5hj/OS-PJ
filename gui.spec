# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)  

a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("data/Blank Space.mp3", "data"),
        ("data/Don't Say.mp3", "data"),  
        ("data/New Romantics.mp3", "data"),
        ("data/Style.mp3", "data") ,
        ("data/Wildest Dreams.mp3", "data"),
        ("data/willow.mp3", "data"),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
