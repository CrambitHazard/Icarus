import pytest
from tts.openvoice_wrapper import OpenVoiceTTS

def test_tts_controls(monkeypatch):
    tts = OpenVoiceTTS()
    # Mock speak to not actually speak
    monkeypatch.setattr(tts, 'engine', type('MockEngine', (), {
        'say': lambda self, text: setattr(tts, '_said', text),
        'runAndWait': lambda self: None,
        'getProperty': lambda self, prop: [],
        'setProperty': lambda self, prop, val: setattr(tts, f'_set_{prop}', val),
    })())
    tts.available = True
    tts.muted = False
    tts.speak("hello")
    assert getattr(tts, '_said', None) == "hello"
    tts.mute()
    assert tts.muted
    tts.unmute()
    assert not tts.muted
    tts.set_speed(150)
    assert getattr(tts, '_set_rate', None) == 150
    tts.set_volume(0.5)
    assert getattr(tts, '_set_volume', None) == 0.5
    tts.set_voice("test")  # Should not error even if no voices 