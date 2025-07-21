import os
import pytest
from actions.read_file import read_file

def test_read_file_txt(tmp_path):
    f = tmp_path / "foo.txt"
    f.write_text("Hello world")
    result = read_file(f"read {f.name}", search_dirs=[str(tmp_path)])
    assert "Hello world" in result

def test_read_file_md(tmp_path):
    f = tmp_path / "bar.md"
    f.write_text("# Title\nContent")
    result = read_file(f"read {f.name}", search_dirs=[str(tmp_path)])
    assert "Title" in result

def test_read_file_csv(tmp_path):
    f = tmp_path / "baz.csv"
    f.write_text("a,b,c\n1,2,3")
    result = read_file(f"read {f.name}", search_dirs=[str(tmp_path)])
    assert "a, b, c" in result
    assert "1, 2, 3" in result
# .docx, .xlsx, .pdf would require test dependencies and/or mocking, so are omitted for brevity 