import pytest
from utils.confirm import confirm_action

def test_confirm_yes(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    assert confirm_action('Proceed?') is True

def test_confirm_no(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    assert confirm_action('Proceed?') is False

def test_confirm_uppercase(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'Y')
    assert confirm_action('Proceed?') is True

def test_confirm_invalid(monkeypatch):
    inputs = iter(['maybe', 'y'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert confirm_action('Proceed?') is True

def test_confirm_empty(monkeypatch):
    inputs = iter(['', 'n'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert confirm_action('Proceed?') is False

def test_confirm_action_persistent(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    assert confirm_action('Persistent session confirm?') is True 