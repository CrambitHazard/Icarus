import pytest
from actions.summarize_pdf import summarize_pdf

class DummyPage:
    def extract_text(self):
        return "This is a test page."

class DummyReader:
    pages = [DummyPage(), DummyPage()]

def test_summarize_pdf(tmp_path, monkeypatch):
    import sys
    sys.modules['PyPDF2'] = type('mod', (), {'PdfReader': lambda f: DummyReader()})
    file = tmp_path / "test.pdf"
    file.write_bytes(b"%PDF-1.4 test")
    summary = summarize_pdf(str(file), max_chars=10)
    assert summary.startswith("This is a t") or summary.startswith("This is a \n")
    assert "[truncated]" in summary
    if 'PyPDF2' in sys.modules:
        del sys.modules['PyPDF2']

def test_pdf_not_found():
    with pytest.raises(ValueError):
        summarize_pdf("nofile.pdf")

def test_pdf_no_text(monkeypatch, tmp_path):
    class DummyPage:
        def extract_text(self):
            return None
    class DummyReader:
        pages = [DummyPage()]
    import sys
    sys.modules['PyPDF2'] = type('mod', (), {'PdfReader': lambda f: DummyReader()})
    file = tmp_path / 'empty.pdf'
    file.write_bytes(b'%PDF-1.4 test')
    result = summarize_pdf(str(file))
    assert 'No extractable text' in result
    if 'PyPDF2' in sys.modules:
        del sys.modules['PyPDF2']

def test_pdf_corrupted(monkeypatch, tmp_path):
    def raise_error(*a, **k):
        raise Exception('corrupted')
    import sys
    sys.modules['PyPDF2'] = type('mod', (), {'PdfReader': raise_error})
    file = tmp_path / 'corrupt.pdf'
    file.write_bytes(b'%PDF-1.4 test')
    with pytest.raises(Exception):
        summarize_pdf(str(file))
    if 'PyPDF2' in sys.modules:
        del sys.modules['PyPDF2']

def test_pypdf2_not_installed(monkeypatch, tmp_path):
    import sys
    sys.modules['PyPDF2'] = None
    file = tmp_path / 'test.pdf'
    file.write_bytes(b'%PDF-1.4 test')
    from importlib import reload
    import actions.summarize_pdf as spdf
    reload(spdf)
    result = spdf.summarize_pdf(str(file))
    assert 'PyPDF2 is required' in result
    if 'PyPDF2' in sys.modules:
        del sys.modules['PyPDF2'] 