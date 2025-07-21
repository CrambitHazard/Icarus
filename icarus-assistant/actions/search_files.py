"""
search_files.py

Searches for files by name, content, or pattern in common directories.
"""

import os
import re
import difflib
from typing import List

def search_files(query: str, search_dirs=None, extensions=None, content_search=False) -> List[str]:
    """Searches for files by name or content. Shows top 3 fuzzy matches if ambiguous.

    Args:
        query (str): File name, pattern, or content to search for.
        search_dirs (list): Directories to search.
        extensions (list): Allowed file extensions.
        content_search (bool): If True, search file contents as well.

    Returns:
        List[str]: List of matching file paths.
    """
    if search_dirs is None:
        search_dirs = ['.', '..', '../..', 'E:/vesavi', 'E:/Ikharos', 'E:/']
    if extensions is None:
        extensions = ['.txt', '.md', '.pdf', '.docx', '.xlsx', '.csv']
    matches = []
    query_lower = query.lower()
    candidates = []
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for fname in os.listdir(d):
            if any(fname.lower().endswith(ext) for ext in extensions):
                candidates.append(os.path.join(d, fname))
                if query_lower in fname.lower():
                    matches.append(os.path.join(d, fname))
                elif content_search:
                    try:
                        with open(os.path.join(d, fname), 'r', encoding='utf-8', errors='ignore') as f:
                            if query_lower in f.read().lower():
                                matches.append(os.path.join(d, fname))
                    except Exception:
                        pass
    # Fuzzy match if not enough direct matches
    if len(matches) < 3 and candidates:
        fuzzy_matches = difflib.get_close_matches(query_lower, [os.path.basename(f) for f in candidates], n=3, cutoff=0.5)
        for m in fuzzy_matches:
            for f in candidates:
                if os.path.basename(f) == m and f not in matches:
                    matches.append(f)
    return matches 

def present_file_matches(matches: List[str]) -> str:
    """Present file matches to the user, showing top 3 if ambiguous.

    Args:
        matches (List[str]): List of matching file paths.

    Returns:
        str: Message to present to the user.
    """
    if not matches:
        return "No matching files found."
    if len(matches) == 1:
        return f"Found file: {os.path.basename(matches[0])}"
    msg = "Multiple files found. Top matches:\n"
    for i, m in enumerate(matches[:3], 1):
        msg += f"{i}. {os.path.basename(m)}\n"
    msg += "Please specify the number or clarify the file name."
    return msg 

def list_files_in_directory(directory: str = '.', extensions: list = None) -> list:
    """Lists files in a directory, optionally filtering by extension.

    Args:
        directory (str): Directory to list files from.
        extensions (list, optional): List of file extensions to include.

    Returns:
        list: List of file names in the directory.
    """
    if not os.path.isdir(directory):
        return []
    files = []
    for fname in os.listdir(directory):
        if extensions:
            if any(fname.lower().endswith(ext) for ext in extensions):
                files.append(fname)
        else:
            files.append(fname)
    return files 

def get_system_info() -> str:
    """Returns a summary of running processes and basic system info.

    Returns:
        str: System/process info summary.
    """
    try:
        import psutil
        procs = [p.info for p in psutil.process_iter(['pid', 'name'])]
        top = '\n'.join([f"{p['pid']}: {p['name']}" for p in procs[:10]])
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent
        return f"Top running processes:\n{top}\nCPU: {cpu}%\nMemory: {mem}%"
    except ImportError:
        try:
            import os
            procs = os.popen('tasklist').read().splitlines()[3:13]
            return 'Top running processes (tasklist):\n' + '\n'.join(procs)
        except Exception as e:
            return f"System info not available: {e}" 