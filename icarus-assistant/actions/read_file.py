"""
read_file.py

Reads and returns the contents of .txt, .md, or .pdf files. Supports spoken file names and fuzzy matching.
"""

import os
import re
import difflib

def spoken_to_filename(spoken: str) -> str:
    """Converts a spoken file name to a real file name.

    Args:
        spoken (str): Spoken file name (e.g., 'eleven labs underscore TDD dot pdf')

    Returns:
        str: File name (e.g., '11labs_TDD.pdf')
    """
    # Map common spoken numbers/words to digits/abbreviations
    replacements = {
        'underscore': '_',
        'dot': '.',
        'dash': '-',
        'space': ' ',
        'eleven labs': '11labs',
        'for': '4',
        'to': '2',
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        'zero': '0',
    }
    s = spoken.lower()
    # Replace multi-word keys first
    for k in sorted(replacements, key=lambda x: -len(x)):
        s = re.sub(rf'\b{k}\b', replacements[k], s)
    # Remove filler words
    s = re.sub(r'\b(for|me|the|a|an|please|open|read)\b', '', s)
    # Remove extra spaces
    s = re.sub(r'\s+', '', s)
    return s

def extract_filename_from_command(command: str) -> str:
    """Extracts the file name (spoken or real) from a user's command after 'read' and up to a file extension.

    Args:
        command (str): The user's voice command.

    Returns:
        str: Extracted file name (spoken form).
    """
    # Find the word 'read' and everything after, up to a file extension
    match = re.search(r'read\s+(.*?\.(?:txt|md|pdf))', command, re.IGNORECASE)
    if match:
        return match.group(1)
    # Fallback: try to find the first .txt/.md/.pdf in the command
    match = re.search(r'(\S+\.(?:txt|md|pdf))', command, re.IGNORECASE)
    if match:
        return match.group(1)
    # Fallback: return everything after 'read'
    if 'read' in command.lower():
        return command.lower().split('read', 1)[1].strip()
    return command.strip()

def fuzzy_find_file(target: str, search_dirs=None, extensions=None) -> str:
    """Fuzzy match the target file name in the search directories.

    Args:
        target (str): Target file name (after spoken-to-filename conversion).
        search_dirs (list): Directories to search.
        extensions (list): Allowed file extensions.

    Returns:
        str: Path to the closest matching file, or raises ValueError if not found.
    """
    if os.path.isabs(target) and os.path.isfile(target):
        return target
    if search_dirs is None:
        search_dirs = ['.', '..', '../..', 'E:/vesavi', 'E:/Ikharos', 'E:/']
    if extensions is None:
        extensions = ['.txt', '.md', '.pdf', '.docx', '.xlsx', '.csv']
    candidates = []
    for d in search_dirs:
        if not os.path.isdir(d):
            continue
        for fname in os.listdir(d):
            if any(fname.lower().endswith(ext) for ext in extensions):
                candidates.append(os.path.join(d, fname))
    print(f"[FileReader] Target: {target}")
    print(f"[FileReader] Candidates: {[os.path.basename(f) for f in candidates]}")
    matches = difflib.get_close_matches(target, [os.path.basename(f) for f in candidates], n=1, cutoff=0.6)
    if matches:
        print(f"[FileReader] Matched: {matches[0]}")
        for f in candidates:
            if os.path.basename(f) == matches[0]:
                return f
    print(f"[FileReader] No match found for '{target}'")
    raise ValueError(f"No file found matching '{target}' in {search_dirs}")

def summarize_text(text: str, max_length: int = 1000) -> str:
    """Summarizes text by returning the first and last parts if too long."""
    if len(text) <= max_length:
        return text
    return (
        text[:max_length // 2]
        + '\n...\n[Summary: content truncated, showing start and end of file]\n...\n'
        + text[-max_length // 2:]
    )

def read_file(user_command: str, search_dirs=None) -> str:
    """Reads and returns the contents of a .txt, .md, .pdf, .docx, .xlsx, or .csv file. Accepts spoken or real file names, with fuzzy matching.

    Args:
        user_command (str): The user's voice command or file name.
        search_dirs (list, optional): Directories to search for the file.

    Returns:
        str: File contents.
    Raises:
        ValueError: If file is not a supported type or does not exist.
        Exception: For other read errors.
    """
    # Extract file name from command
    spoken_name = extract_filename_from_command(user_command)
    fname = spoken_to_filename(spoken_name)
    try:
        real_path = fuzzy_find_file(fname, search_dirs=search_dirs, extensions=['.txt', '.md', '.pdf', '.docx', '.xlsx', '.csv'])
    except ValueError as e:
        raise ValueError(f"File not found for '{user_command}': {e}")
    try:
        if real_path.endswith('.pdf'):
            try:
                import PyPDF2
            except ImportError:
                return "PyPDF2 is required to read PDF files. Please install it."
            with open(real_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() or ''
                return summarize_text(text)
        elif real_path.endswith('.docx'):
            try:
                import docx
            except ImportError:
                return "python-docx is required to read DOCX files. Please install it."
            doc = docx.Document(real_path)
            text = '\n'.join([p.text for p in doc.paragraphs])
            return summarize_text(text)
        elif real_path.endswith('.xlsx'):
            try:
                import openpyxl
            except ImportError:
                return "openpyxl is required to read XLSX files. Please install it."
            wb = openpyxl.load_workbook(real_path, read_only=True)
            text = ''
            for sheet in wb.worksheets:
                text += f"[Sheet: {sheet.title}]\n"
                for row in sheet.iter_rows(values_only=True):
                    text += ', '.join([str(cell) if cell is not None else '' for cell in row]) + '\n'
            return summarize_text(text)
        elif real_path.endswith('.csv'):
            import csv
            with open(real_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                text = ''
                for row in reader:
                    text += ', '.join(row) + '\n'
                return summarize_text(text)
        elif real_path.endswith('.txt') or real_path.endswith('.md'):
            with open(real_path, 'r', encoding='utf-8') as f:
                text = f.read()
                return summarize_text(text)
        else:
            raise ValueError("Only .txt, .md, .pdf, .docx, .xlsx, and .csv files are supported.")
    except Exception as e:
        print(f"Error reading file: {e}")
        raise
