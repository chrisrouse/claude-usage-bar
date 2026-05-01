# PyInstaller spec — invoked by `make app`
# Produces a macOS .app bundle via --windowed (no terminal window).

import os

block_cipher = None

a = Analysis(
    ["claude_usage_bar/__main__.py"],
    pathex=["."],
    binaries=[],
    datas=[],
    hiddenimports=["rumps"],
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
    [],
    exclude_binaries=True,
    name="Claude Usage Bar",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,       # no terminal window
    icon="assets/AppIcon.icns",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="Claude Usage Bar",
)

app = BUNDLE(
    coll,
    name="Claude Usage Bar.app",
    icon="assets/AppIcon.icns",
    bundle_identifier="us.chrisrouse.claude-usage-bar",
    info_plist={
        "CFBundleName": "Claude Usage Bar",
        "CFBundleDisplayName": "Claude Usage Bar",
        "CFBundleVersion": "0.1.0",
        "CFBundleShortVersionString": "0.1.0",
        "LSUIElement": True,        # status bar only — hides from Dock
        "NSHumanReadableCopyright": "© 2026 Chris Rouse",
    },
)
