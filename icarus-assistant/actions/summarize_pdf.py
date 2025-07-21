"""
summarize_pdf.py

Summarize PDF files for Icarus Assistant Phase 2.
"""

import os
from typing import Optional

def summarize_pdf(file_path: str, max_chars: int = 1000) -> str:
    """Summarize the contents of a PDF file.

    Args:
        file_path (str): Path to the PDF file.
        max_chars (int): Maximum number of characters in the summary.

    Returns:
        str: Summary of the PDF.
    Raises:
        ValueError: If file is not a PDF or not found.
        Exception: For other read errors.
    """
    if not os.path.isfile(file_path) or not file_path.lower().endswith('.pdf'):
        raise ValueError(f"PDF file not found: {file_path}")
    try:
        import PyPDF2
    except ImportError:
        return "PyPDF2 is required to summarize PDF files. Please install it."
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text() or ''
        if not text:
            return "No extractable text found in PDF."
        # Simple summary: first max_chars characters
        summary = text[:max_chars]
        if len(text) > max_chars:
            summary += '\n... [truncated]'
        return summary
    except Exception as e:
        raise Exception(f"PDF summarization failed: {e}") 