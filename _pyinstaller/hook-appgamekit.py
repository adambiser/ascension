import os
import struct
runtime_bits = struct.calcsize("P") * 8

agk_import = 'appgamekit.' + ('_x86' if runtime_bits == 32 else '_x64') + '.appgamekit'
hiddenimports = ['typing', 'ctypes', agk_import]
# Special paths used by AppGameKit.
datas = [(d, d) for d in ['media', 'Plugins'] if os.path.isdir(d)]
if os.path.isfile('icon.ico'):
    datas.append(('icon.ico', '.'))
