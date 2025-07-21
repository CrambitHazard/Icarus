"""
move_files.py

Move or copy files for Icarus Assistant Phase 2.
"""

import os
import shutil

def move_file(src: str, dst: str, copy: bool = False) -> str:
    """Move or copy a file from src to dst.

    Args:
        src (str): Source file path.
        dst (str): Destination file path.
        copy (bool): If True, copy instead of move.

    Returns:
        str: Result message.
    Raises:
        ValueError: If src does not exist or dst is invalid.
        Exception: For other file errors.
    """
    if not os.path.isfile(src):
        raise ValueError(f"Source file not found: {src}")
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    try:
        if copy:
            shutil.copy2(src, dst)
            return f"Copied {src} to {dst}."
        else:
            shutil.move(src, dst)
            return f"Moved {src} to {dst}."
    except Exception as e:
        raise Exception(f"Move/copy failed: {e}") 