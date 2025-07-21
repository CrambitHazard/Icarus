import pytest
from orchestrator.wakeword_listener import WakewordListener

class DummyWakewordListener(WakewordListener):
    def __init__(self, responses):
        super().__init__()
        self.responses = responses
        self.call_count = 0
    def listen_for_wakeword(self, wakeword="icarus", feedback=False):
        resp = self.responses[self.call_count] if self.call_count < len(self.responses) else False
        self.call_count += 1
        return resp

def test_wakeword_detected():
    listener = DummyWakewordListener([True])
    assert listener.listen_for_wakeword() is True

def test_wakeword_not_detected():
    listener = DummyWakewordListener([False])
    assert listener.listen_for_wakeword() is False

def test_wakeword_multiple_calls():
    listener = DummyWakewordListener([False, True])
    assert listener.listen_for_wakeword() is False
    assert listener.listen_for_wakeword() is True 