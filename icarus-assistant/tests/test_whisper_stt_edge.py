import pytest
from stt.whisper_wrapper import WhisperSTT
import wave
import numpy as np

@pytest.fixture
def stt():
    return WhisperSTT()

def test_silent_audio(tmp_path, stt):
    # Create a valid silent wav file
    fname = tmp_path / "silent.wav"
    with wave.open(str(fname), 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        data = (np.zeros(16000)).astype(np.int16).tobytes()
        wf.writeframes(data)
    result = stt.transcribe(str(fname))
    assert isinstance(result, str)

def test_corrupted_audio(tmp_path, stt):
    fname = tmp_path / "corrupt.wav"
    fname.write_bytes(b"notawav")
    with pytest.raises(Exception):
        stt.transcribe(str(fname))

def test_model_load_error(monkeypatch):
    monkeypatch.setattr("whisper.load_model", lambda *a, **k: (_ for _ in ()).throw(Exception("fail")))
    with pytest.raises(Exception):
        WhisperSTT()

def test_wakeword_detection(monkeypatch):
    from orchestrator.wakeword_listener import WakewordListener
    # Monkeypatch recognizer and mic
    class DummyRecognizer:
        def adjust_for_ambient_noise(self, source): pass
        def listen(self, source, timeout=None, phrase_time_limit=None): return b''
        def recognize_google(self, audio): return 'icarus'
    class DummyMic:
        def __enter__(self): return self
        def __exit__(self, exc_type, exc_val, exc_tb): pass
    called = {'flag': False}
    def cb(): called['flag'] = True; return True
    listener = WakewordListener()
    listener.recognizer = DummyRecognizer()
    listener.mic = DummyMic()
    assert listener.listen_for_wakeword(callback=cb) is True
    assert called['flag'] 