import os
import pytest
from actions.search_files import search_files, present_file_matches, list_files_in_directory

def test_search_files_txt(tmp_path):
    # Create test files
    f1 = tmp_path / "alpha.txt"
    f2 = tmp_path / "beta.txt"
    f1.write_text("Hello Alpha")
    f2.write_text("Hello Beta")
    # Should find exact match
    matches = search_files("alpha.txt", search_dirs=[str(tmp_path)])
    assert any("alpha.txt" in m for m in matches)
    # Should fuzzy match
    matches = search_files("alfa.txt", search_dirs=[str(tmp_path)])
    assert any("alpha.txt" in m for m in matches)

def test_present_file_matches():
    matches = ["/a/alpha.txt", "/b/beta.txt", "/c/gamma.txt"]
    msg = present_file_matches(matches)
    assert "Multiple files found" in msg
    assert "1. alpha.txt" in msg
    assert "2. beta.txt" in msg
    assert "3. gamma.txt" in msg
    msg = present_file_matches(["/a/alpha.txt"])
    assert "Found file" in msg
    msg = present_file_matches([])
    assert "No matching files" in msg

def test_list_files_in_directory(tmp_path):
    (tmp_path / "foo.txt").write_text("foo")
    (tmp_path / "bar.md").write_text("bar")
    (tmp_path / "baz.pdf").write_text("baz")
    files = list_files_in_directory(str(tmp_path), extensions=[".txt", ".md"])
    assert "foo.txt" in files
    assert "bar.md" in files
    assert "baz.pdf" not in files 