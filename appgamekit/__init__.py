import importlib
import struct

# Load the appgamekit module based upon whether running under a 32- or 64-bit runtime.
_runtime_bits = struct.calcsize("P") * 8
if _runtime_bits == 32:
    _module_path = "._x86.appgamekit"
elif _runtime_bits == 64:
    _module_path = "._x64.appgamekit"
else:
    raise ImportError("Unsupported runtime.  Must be x86 or x64.")

# Bring in everything including items starting with an underscore.
_appgamekit = importlib.import_module(_module_path, __name__)
globals().update(_appgamekit.__dict__)

# noinspection PyUnresolvedReferences
# print(__version__)

del importlib
del struct
del _runtime_bits
del _module_path
del _appgamekit
