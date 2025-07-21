import os
import pytest
from actions.search_files import search_files

def test_no_dirs():
    matches = search_files("foo", search_dirs=["/nonexistentdir"])
    assert matches == []

def test_ambiguous_matches(tmp_path):
    (tmp_path / "foo.txt").write_text("a")
    (tmp_path / "f00.txt").write_text("b")
    matches = search_files("foo", search_dirs=[str(tmp_path)])
    assert len(matches) >= 1

def test_special_char_files(tmp_path):
    (tmp_path / "foo bar.txt").write_text("a")
    matches = search_files("foo bar", search_dirs=[str(tmp_path)])
    assert any("foo bar.txt" in m for m in matches)

def test_hidden_files(tmp_path):
    (tmp_path / ".hidden.txt").write_text("a")
    matches = search_files("hidden", search_dirs=[str(tmp_path)])
    assert any(".hidden.txt" in m for m in matches)

def test_no_matches(tmp_path):
    result = search_files('notfound', search_dirs=[str(tmp_path)])
    assert result == []

def test_multiple_matches(tmp_path):
    (tmp_path / 'a.txt').write_text('x')
    (tmp_path / 'b.txt').write_text('x')
    result = search_files('a', search_dirs=[str(tmp_path)])
    assert any('a.txt' in f for f in result)
    result = search_files('txt', search_dirs=[str(tmp_path)])
    assert len(result) >= 2

def test_empty_directory(tmp_path):
    result = search_files('anything', search_dirs=[str(tmp_path)])
    assert result == []

def test_special_characters(tmp_path):
    (tmp_path / 'we!rd.txt').write_text('x')
    result = search_files('!', search_dirs=[str(tmp_path)])
    assert any('we!rd.txt' in f for f in result) 