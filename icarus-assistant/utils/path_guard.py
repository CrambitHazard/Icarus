"""
path_guard.py

Utility for folder access rules and path safety checks.
"""

import os

def is_safe_path(path: str, allowed_dirs: list = None) -> bool:
    """Checks if a path is within allowed directories.

    Args:
        path (str): The file or folder path to check.
        allowed_dirs (list): List of allowed base directories.

    Returns:
        bool: True if path is safe, False otherwise.
    """
    if allowed_dirs is None:
        allowed_dirs = ['.', 'E:/vesavi', 'E:/Ikharos']
    abs_path = os.path.abspath(path)
    for base in allowed_dirs:
        if abs_path.startswith(os.path.abspath(base)):
            return True
    print(f"[PathGuard] Unsafe path: {abs_path}")
    return False 