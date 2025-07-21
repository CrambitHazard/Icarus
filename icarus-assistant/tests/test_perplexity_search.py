import pytest
from actions.perplexity_search import PerplexitySearch

class DummyKeyboard:
    def __init__(self):
        self.actions = []
    def press_hotkey(self, *keys):
        self.actions.append(('hotkey', keys))
    def type_text(self, text, delay=0.1):
        self.actions.append(('type', text))
    def press_key(self, key):
        self.actions.append(('key', key))
    def wait(self, seconds):
        self.actions.append(('wait', seconds))

@pytest.fixture
def monkeypatch_keyboard(monkeypatch):
    dummy = DummyKeyboard()
    monkeypatch.setattr('actions.perplexity_search.KeyboardController', lambda: dummy)
    return dummy

@pytest.fixture
def monkeypatch_pyperclip(monkeypatch):
    clipboard = {'value': ''}
    monkeypatch.setattr('pyperclip.paste', lambda: clipboard['value'])
    return clipboard

def test_perplexity_search_basic(monkeypatch_keyboard, monkeypatch_pyperclip):
    monkeypatch_pyperclip['value'] = 'Search result!'
    ps = PerplexitySearch()
    result = ps.search('test query')
    assert result == 'Search result!'
    # Check that hotkey, typing, enter, and clipboard actions were triggered
    actions = monkeypatch_keyboard.actions
    assert any(a[0] == 'hotkey' for a in actions)
    assert any(a[0] == 'type' and a[1] == 'test query' for a in actions)
    assert any(a[0] == 'key' and a[1] == 'enter' for a in actions)

def test_perplexity_search_no_clipboard(monkeypatch_keyboard, monkeypatch_pyperclip):
    monkeypatch_pyperclip['value'] = ''
    ps = PerplexitySearch()
    result = ps.search('test query')
    assert '[Perplexity search: No result copied from clipboard]' in result 