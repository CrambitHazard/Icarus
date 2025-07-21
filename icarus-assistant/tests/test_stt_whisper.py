import pytest
from unittest.mock import patch, MagicMock
from stt.whisper_wrapper import WhisperSTT

def test_transcribe_normal(monkeypatch):
    stt = WhisperSTT()
    monkeypatch.setattr(stt, 'model', MagicMock())
    stt.model.transcribe.return_value = {'text': 'hello world'}
    assert stt.transcribe('audio.wav') == 'hello world'

def test_transcribe_silent(monkeypatch):
    stt = WhisperSTT()
    monkeypatch.setattr(stt, 'model', MagicMock())
    stt.model.transcribe.return_value = {'text': ''}
    assert stt.transcribe('silent.wav') == ''

def test_transcribe_noisy(monkeypatch):
    stt = WhisperSTT()
    monkeypatch.setattr(stt, 'model', MagicMock())
    stt.model.transcribe.return_value = {'text': 'background noise'}
    assert stt.transcribe('noisy.wav') == 'background noise'

def test_transcribe_non_english(monkeypatch):
    stt = WhisperSTT()
    monkeypatch.setattr(stt, 'model', MagicMock())
    stt.model.transcribe.return_value = {'text': 'bonjour'}
    assert stt.transcribe('french.wav') == 'bonjour'

def test_transcribe_corrupted(monkeypatch):
    stt = WhisperSTT()
    monkeypatch.setattr(stt, 'model', MagicMock(side_effect=Exception('corrupted')))
    with pytest.raises(Exception):
        stt.transcribe('corrupt.wav') 