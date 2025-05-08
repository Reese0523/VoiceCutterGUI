# hook-restore-ctypes.py
import sys, ctypes

if getattr(sys, 'frozen', False):
    try:
        from PyInstaller.loader import pyimod03_ctypes
        ctypes.CDLL = pyimod03_ctypes.OriginalCDLL
    except:
        pass
