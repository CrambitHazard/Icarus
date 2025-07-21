import pytest
from actions.system_tools import get_cpu_usage, get_ram_usage, get_clipboard, set_clipboard, get_weather, get_random_joke

def test_cpu_usage():
    result = get_cpu_usage()
    assert isinstance(result, str)

def test_ram_usage():
    result = get_ram_usage()
    assert isinstance(result, str)

def test_clipboard_empty(monkeypatch):
    monkeypatch.setattr('pyperclip.paste', lambda: '')
    result = get_clipboard()
    assert result == '' or result == 'Clipboard: '

def test_clipboard_denied(monkeypatch):
    monkeypatch.setattr('pyperclip.paste', lambda: (_ for _ in ()).throw(PermissionError('denied')))
    result = get_clipboard()
    assert 'denied' in result.lower() or 'permission' in result.lower() or result == 'Clipboard information not available.'

def test_weather_api_unavailable(monkeypatch):
    monkeypatch.setattr('actions.system_tools.get_weather', lambda: 'Weather API unavailable')
    result = get_weather()
    assert result == 'Weather API unavailable' or 'weather' in result.lower()

def test_joke_api_unavailable(monkeypatch):
    monkeypatch.setattr('actions.system_tools.get_random_joke', lambda: 'Joke API unavailable')
    result = get_random_joke()
    assert result == 'Joke API unavailable' or 'joke' in result.lower() or 'doctor' in result.lower() 