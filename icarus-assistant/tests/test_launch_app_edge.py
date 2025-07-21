import pytest
from actions.launch_app import launch_app, update_app_map
import os

def test_app_not_installed():
    result = launch_app("nonexistentapp")
    assert "not found" in result or "Failed" in result

def test_permission_denied(monkeypatch):
    monkeypatch.setattr(os, "startfile", lambda *a, **k: (_ for _ in ()).throw(PermissionError))
    result = launch_app("notepad")
    assert "Failed" in result

def test_path_with_spaces(monkeypatch):
    monkeypatch.setattr(os, "startfile", lambda path: path)
    update_app_map("test app", "C:/Program Files/Test App/testapp.exe")
    result = launch_app("test app")
    assert "Launched" in result

def test_app_not_found():
    from actions.launch_app import launch_app
    result = launch_app('nonexistentapp')
    assert 'not found' in result.lower() or 'could not' in result.lower()

def test_invalid_path(monkeypatch):
    from actions.launch_app import launch_app
    monkeypatch.setattr('os.startfile', lambda *a, **k: (_ for _ in ()).throw(FileNotFoundError('invalid')))
    result = launch_app('invalidpath')
    assert 'invalid' in result.lower() or 'not found' in result.lower()

def test_permission_denied(monkeypatch):
    from actions.launch_app import launch_app
    monkeypatch.setattr('os.startfile', lambda *a, **k: (_ for _ in ()).throw(PermissionError('denied')))
    result = launch_app('notepad')
    assert 'denied' in result.lower() or 'permission' in result.lower()

def test_ambiguous_app(monkeypatch):
    from actions.launch_app import launch_app
    monkeypatch.setattr('actions.launch_app.get_app_names', lambda: ['notepad', 'notepad++'])
    result = launch_app('notepad')
    assert 'notepad' in result.lower() 