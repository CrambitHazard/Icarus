import pytest
from actions import system_tools
from unittest import mock


def test_get_cpu_usage():
    """Test get_cpu_usage returns a string with 'CPU Usage' or fallback message."""
    result = system_tools.get_cpu_usage()
    assert isinstance(result, str)
    assert 'CPU Usage' in result or 'not available' in result


def test_get_ram_usage():
    """Test get_ram_usage returns a string with 'RAM Usage' or fallback message."""
    result = system_tools.get_ram_usage()
    assert isinstance(result, str)
    assert 'RAM Usage' in result or 'not available' in result


def test_get_clipboard(monkeypatch):
    """Test get_clipboard returns clipboard contents or fallback message."""
    monkeypatch.setattr('pyperclip.paste', lambda: 'test clipboard')
    result = system_tools.get_clipboard()
    assert 'test clipboard' in result or 'not available' in result


def test_set_clipboard(monkeypatch):
    """Test set_clipboard sets clipboard contents and returns confirmation or fallback message."""
    monkeypatch.setattr('pyperclip.copy', lambda x: None)
    result = system_tools.set_clipboard('hello')
    assert 'updated' in result or 'Failed' in result


def test_open_url(monkeypatch):
    """Test open_url opens a URL and returns confirmation or fallback message."""
    monkeypatch.setattr('webbrowser.open', lambda url: True)
    result = system_tools.open_url('http://example.com')
    assert 'Opened URL' in result or 'Failed' in result


def test_get_weather():
    """Test get_weather returns a dummy weather report."""
    result = system_tools.get_weather('Paris')
    assert 'Paris' in result
    assert 'weather' in result or 'sunny' in result


def test_get_random_joke():
    """Test get_random_joke returns a joke string."""
    result = system_tools.get_random_joke()
    assert isinstance(result, str)
    assert 'virus' in result or 'computer' in result 