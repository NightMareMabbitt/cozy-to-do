import sys
import subprocess 

def detect_sytem_dark_mode():
    try:
        if sys.platform == 'darwin':
            result = subprocess.run(
                ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                capture_output=True, text=True
            )
            return 'Dark' in result.stdout
    except Exception:
        pass
    return False

def setup_dpi_awareness():
    if sys.platform == 'win32':
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)  
        except Exception:
            pass