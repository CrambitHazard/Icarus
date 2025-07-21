import os
import pytest
from actions.edit_text import edit_text

def setup_file(tmp_path, content):
    file = tmp_path / "test.txt"
    file.write_text(content)
    return str(file)

def test_replace_line(tmp_path):
    file = setup_file(tmp_path, "a\nb\nc\n")
    result = edit_text(file, "replace", "z", 2)
    assert result == "Replace successful."
    assert open(file).readlines()[1].strip() == "z"

def test_append_line(tmp_path):
    file = setup_file(tmp_path, "a\nb\n")
    result = edit_text(file, "append", "c")
    assert result == "Append successful."
    assert open(file).readlines()[-1].strip() == "c"

def test_delete_line(tmp_path):
    file = setup_file(tmp_path, "a\nb\nc\n")
    result = edit_text(file, "delete", line=2)
    assert result == "Delete successful."
    lines = open(file).readlines()
    assert lines == ["a\n", "c\n"]

def test_invalid_operation(tmp_path):
    file = setup_file(tmp_path, "a\n")
    with pytest.raises(ValueError):
        edit_text(file, "invalid")

def test_file_not_found():
    with pytest.raises(ValueError):
        edit_text("nofile.txt", "replace", "x", 1)

def test_line_out_of_range(tmp_path):
    file = setup_file(tmp_path, "a\nb\n")
    with pytest.raises(ValueError):
        edit_text(file, "replace", "z", 10)
    with pytest.raises(ValueError):
        edit_text(file, "delete", line=10)

def test_empty_file_replace(tmp_path):
    file = setup_file(tmp_path, "")
    with pytest.raises(ValueError):
        edit_text(file, "replace", "z", 1)

def test_permission_denied(monkeypatch, tmp_path):
    file = setup_file(tmp_path, "a\nb\n")
    def raise_permission(*a, **k):
        raise PermissionError("Permission denied")
    monkeypatch.setattr("builtins.open", raise_permission)
    with pytest.raises(Exception) as e:
        edit_text(file, "replace", "z", 1)
    assert "Permission denied" in str(e.value) 