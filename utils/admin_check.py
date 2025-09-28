import os
import sys

def is_admin():
    """
    Check if the program is running as administrator/root.
    Returns True if admin, else False.
    """
    try:
        if os.name == "nt":  # Windows
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:  # Linux / Mac
            return os.getuid() == 0
    except Exception:
        return False
