import pytest
from unittest.mock import patch, MagicMock
from tts.openvoice_wrapper import OpenVoiceTTS

def test_speak_normal(monkeypatch):
    tts = OpenVoiceTTS()
    monkeypatch.setattr(tts, 'engine', MagicMock())
    tts.engine.say = MagicMock()
    tts.engine.runAndWait = MagicMock()
    tts.speak('hello')
    tts.engine.say.assert_called_with('hello')

def test_speak_empty(monkeypatch):
    tts = OpenVoiceTTS()
    monkeypatch.setattr(tts, 'engine', MagicMock())
    tts.engine.say = MagicMock()
    tts.engine.runAndWait = MagicMock()
    tts.speak('')
    tts.engine.say.assert_called_with('')

def test_speak_long(monkeypatch):
    tts = OpenVoiceTTS()
    monkeypatch.setattr(tts, 'engine', MagicMock())
    tts.engine.say = MagicMock()
    tts.engine.runAndWait = MagicMock()
    long_text = 'a' * 10000
    tts.speak(long_text)
    tts.engine.say.assert_called_with(long_text)

def test_speak_special_chars(monkeypatch):
    tts = OpenVoiceTTS()
    monkeypatch.setattr(tts, 'engine', MagicMock())
    tts.engine.say = MagicMock()
    tts.engine.runAndWait = MagicMock()
    tts.speak('!@#$%^&*()')
    tts.engine.say.assert_called_with('!@#$%^&*()')

def test_engine_unavailable(monkeypatch, capsys):
    tts = OpenVoiceTTS()
    monkeypatch.setattr(tts, 'engine', None)
    tts.speak('hello')
    out = capsys.readouterr().out
    assert 'pyttsx3 not available' in out or 'TTS fallback' in out 