import pytest
import types
from utils.keyboard_controller import KeyboardController

class DummyPyAutoGUI:
    def __init__(self):
        self.calls = []
    def hotkey(self, *keys):
        self.calls.append(('hotkey', keys))
    def write(self, text, interval=0.1):
        self.calls.append(('write', text, interval))
    def press(self, key):
        self.calls.append(('press', key))

def test_press_hotkey(monkeypatch):
    dummy = DummyPyAutoGUI()
    monkeypatch.setattr('pyautogui.hotkey', dummy.hotkey)
    kc = KeyboardController()
    kc.press_hotkey('ctrl', 'shift', 'p')
    assert dummy.calls == [('hotkey', ('ctrl', 'shift', 'p'))]

def test_type_text(monkeypatch):
    dummy = DummyPyAutoGUI()
    monkeypatch.setattr('pyautogui.write', dummy.write)
    kc = KeyboardController()
    kc.type_text('hello', delay=0.2)
    assert dummy.calls == [('write', 'hello', 0.2)]

def test_press_key(monkeypatch):
    dummy = DummyPyAutoGUI()
    monkeypatch.setattr('pyautogui.press', dummy.press)
    kc = KeyboardController()
    kc.press_key('enter')
    assert dummy.calls == [('press', 'enter')]

def test_wait(monkeypatch):
    called = {}
    def fake_sleep(seconds):
        called['seconds'] = seconds
    monkeypatch.setattr('time.sleep', fake_sleep)
    kc = KeyboardController()
    kc.wait(1.5)
    assert called['seconds'] == 1.5 