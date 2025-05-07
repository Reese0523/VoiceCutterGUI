# -*- mode: python -*-
block_cipher = None

a = Analysis(
    ['voice_cutter_gui.py'],
    pathex=['.'],
    datas=[],
    hiddenimports=['moviepy.editor','whisper','tqdm'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
)
p = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    p,
    a.scripts,
    [],
    exclude_binaries=True,
    name='voice_cutter_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='voice_cutter_gui.dist'
)
