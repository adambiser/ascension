# -*- mode: python -*-
import os
import struct
runtime_bits = struct.calcsize("P") * 8

scripts = ['main.py']
exe_name = 'Ascension'
exe_icon = 'icon.ico'

folder_name = 'Ascension' + ('-win86' if runtime_bits == 32 else '-win64')
# UCRT files need to be included so Windows 10 builds work on Windows 7.
ucrt_path = 'ucrt/' + ('x86' if runtime_bits == 32 else 'x64')

block_cipher = None

a = Analysis(scripts,
             pathex=[ucrt_path],
             binaries=[],
             datas=[('credits.txt', '.')],
			 # Imports used by the appgamekit module.
             hiddenimports=[],
             hookspath=['_pyinstaller'],
             runtime_hooks=['_pyinstaller/use_lib.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name=exe_name,
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon=exe_icon)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=folder_name)
