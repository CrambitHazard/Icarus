import os
import pytest
from actions.read_file import read_file

def test_file_not_found():
    with pytest.raises(ValueError):
        read_file('nofile.txt')

def test_empty_file(tmp_path):
    file = tmp_path / 'empty.txt'
    file.write_text('')
    result = read_file(str(file))
    assert result.strip() == '' or 'empty' in result.lower()

def test_unsupported_extension(tmp_path):
    file = tmp_path / 'file.exe'
    file.write_text('data')
    with pytest.raises(ValueError):
        read_file(str(file))

def test_permission_denied(monkeypatch, tmp_path):
    file = tmp_path / 'file.txt'
    file.write_text('data')
    def raise_permission(*a, **k):
        raise PermissionError('Permission denied')
    monkeypatch.setattr('builtins.open', raise_permission)
    with pytest.raises(Exception) as e:
        read_file(str(file))
    assert 'Permission denied' in str(e.value)

def test_unsupported_format(tmp_path):
    f = tmp_path / "foo.exe"
    f.write_text("binary")
    with pytest.raises(ValueError):
        read_file(f"read {f.name}", search_dirs=[str(tmp_path)])

def test_large_file(tmp_path):
    f = tmp_path / "big.txt"
    f.write_text("A" * 1000000)
    result = read_file(f"read {f.name}", search_dirs=[str(tmp_path)])
    assert result.startswith("A") 