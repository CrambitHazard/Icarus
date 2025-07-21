import pytest
from tts.openvoice_wrapper import OpenVoiceTTS

@pytest.fixture
def tts():
    return OpenVoiceTTS()

def test_invalid_voice(tts):
    tts.set_voice("nonexistentvoice")  # Should not raise

def test_extreme_volume(tts):
    tts.set_volume(0.0)
    tts.set_volume(1.0)
    tts.set_volume(-1.0)
    tts.set_volume(2.0)

def test_extreme_speed(tts):
    tts.set_speed(10)
    tts.set_speed(1000)

def test_muted(tts, monkeypatch):
    tts.mute()
    monkeypatch.setattr(tts, 'engine', type('MockEngine', (), {'say': lambda self, text: (_ for _ in ()).throw(Exception("Should not speak when muted")), 'runAndWait': lambda self: None})())
    tts.speak("should not speak")  # Should not raise

def test_pyttsx3_not_available(monkeypatch):
    monkeypatch.setattr("pyttsx3.init", lambda: (_ for _ in ()).throw(ImportError))
    tts = OpenVoiceTTS()
    assert not tts.available 