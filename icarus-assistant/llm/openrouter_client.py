"""
openrouter_client.py

Client for interacting with OpenRouter LLM API via direct HTTP requests.
"""

import requests

class OpenRouterClient:
    """Client for OpenRouter LLM API.

    Methods:
        query(prompt: str) -> str: Sends prompt to LLM and returns response.
    """
    def __init__(self, api_key: str, model: str):
        """Initializes the client with API key and model.

        Args:
            api_key (str): OpenRouter API key.
            model (str): Model name to use.
        """
        self.api_key = api_key
        self.model = model
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        if self.api_key:
            print(f"[LLM] API Key loaded: {self.api_key[:10]}... (length: {len(self.api_key)})")
        else:
            print("[LLM] No API key found!")

    def query(self, prompt: str) -> str:
        """Sends a prompt to the LLM and returns the response.

        Args:
            prompt (str): The prompt to send.

        Returns:
            str: LLM response.
        Raises:
            Exception: If API call fails or response is invalid.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        try:
            response = requests.post(self.api_url, json=data, headers=headers, timeout=30)
            print(f"[LLM] Status: {response.status_code}")
            if response.status_code != 200:
                print(f"[LLM] Response: {response.text}")
            response.raise_for_status()
            result = response.json()
            # Extract the response text (assuming OpenAI-compatible format)
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"Error querying OpenRouter LLM: {e}")
            raise
