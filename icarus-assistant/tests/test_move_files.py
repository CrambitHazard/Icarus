import os
import pytest
from actions.move_files import move_file

def test_move_file(tmp_path):
    src = tmp_path / "a.txt"
    dst = tmp_path / "b.txt"
    src.write_text("hello")
    result = move_file(str(src), str(dst))
    assert result.startswith("Moved")
    assert os.path.exists(dst)
    assert not os.path.exists(src)

def test_copy_file(tmp_path):
    src = tmp_path / "a.txt"
    dst = tmp_path / "b.txt"
    src.write_text("hello")
    result = move_file(str(src), str(dst), copy=True)
    assert result.startswith("Copied")
    assert os.path.exists(dst)
    assert os.path.exists(src)

def test_move_file_not_found(tmp_path):
    with pytest.raises(ValueError):
        move_file(str(tmp_path / "nofile.txt"), str(tmp_path / "b.txt"))

def test_move_to_directory(tmp_path):
    src = tmp_path / "a.txt"
    dst_dir = tmp_path / "subdir"
    dst_dir.mkdir()
    src.write_text("hello")
    result = move_file(str(src), str(dst_dir))
    assert result.startswith("Moved")
    assert (dst_dir / "a.txt").exists()

def test_overwrite_existing_file(tmp_path):
    src = tmp_path / "a.txt"
    dst = tmp_path / "b.txt"
    src.write_text("hello")
    dst.write_text("old")
    result = move_file(str(src), str(dst))
    assert result.startswith("Moved")
    assert open(dst).read() == "hello"

def test_permission_denied(monkeypatch, tmp_path):
    src = tmp_path / "a.txt"
    dst = tmp_path / "b.txt"
    src.write_text("hello")
    def raise_permission(*a, **k):
        raise PermissionError("Permission denied")
    import shutil
    monkeypatch.setattr(shutil, "move", raise_permission)
    with pytest.raises(Exception) as e:
        move_file(str(src), str(dst))
    assert "Permission denied" in str(e.value) 