import bpy
import sys
try:
    bpy.ops.file.unpack_all(method='USE_LOCAL')
    print("Unpacked successfully.")
except Exception as e:
    print(e)
    sys.exit(1)
