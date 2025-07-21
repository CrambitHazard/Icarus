import pytest
from unittest.mock import patch, MagicMock
from llm.openrouter_client import OpenRouterClient

def test_llm_normal(monkeypatch):
    client = OpenRouterClient(api_key='dummy', model='test-model')
    monkeypatch.setattr(client, 'query', MagicMock(return_value='response'))
    assert client.query('hello') == 'response'

def test_llm_empty_prompt(monkeypatch):
    client = OpenRouterClient(api_key='dummy', model='test-model')
    monkeypatch.setattr(client, 'query', MagicMock(return_value=''))
    assert client.query('') == ''

def test_llm_long_prompt(monkeypatch):
    client = OpenRouterClient(api_key='dummy', model='test-model')
    long_prompt = 'a' * 10000
    monkeypatch.setattr(client, 'query', MagicMock(return_value='long response'))
    assert client.query(long_prompt) == 'long response'

def test_llm_api_fail(monkeypatch):
    client = OpenRouterClient(api_key='dummy', model='test-model')
    monkeypatch.setattr(client, 'query', MagicMock(side_effect=Exception('fail')))
    with pytest.raises(Exception):
        client.query('fail')

def test_llm_invalid_key(monkeypatch):
    client = OpenRouterClient(api_key='dummy', model='test-model')
    monkeypatch.setattr(client, 'query', MagicMock(side_effect=Exception('invalid key')))
    with pytest.raises(Exception):
        client.query('test') 