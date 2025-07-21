"""
edit_text.py

Edit text files: replace, append, or delete lines/sections. Used by Icarus Assistant Phase 2.
"""

import os
from typing import Optional

def edit_text(file_path: str, operation: str, content: Optional[str] = None, line: Optional[int] = None) -> str:
    """Edit a text file by replacing, appending, or deleting content.

    Args:
        file_path (str): Path to the file to edit.
        operation (str): 'replace', 'append', or 'delete'.
        content (Optional[str]): Content to write (for replace/append).
        line (Optional[int]): Line number for replace/delete (1-based).

    Returns:
        str: Result message.
    Raises:
        ValueError: If operation is invalid or file not found.
        Exception: For other file errors.
    """
    if not os.path.isfile(file_path):
        raise ValueError(f"File not found: {file_path}")
    if operation not in ("replace", "append", "delete"):
        raise ValueError(f"Invalid operation: {operation}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        if operation == "replace":
            if line is None or content is None:
                raise ValueError("Line and content required for replace.")
            if not (1 <= line <= len(lines)):
                raise ValueError("Line out of range.")
            lines[line-1] = content + '\n'
        elif operation == "append":
            if content is None:
                raise ValueError("Content required for append.")
            lines.append(content + '\n')
        elif operation == "delete":
            if line is None:
                raise ValueError("Line required for delete.")
            if not (1 <= line <= len(lines)):
                raise ValueError("Line out of range.")
            del lines[line-1]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return f"{operation.capitalize()} successful."
    except ValueError:
        raise
    except Exception as e:
        raise Exception(f"Edit failed: {e}") 