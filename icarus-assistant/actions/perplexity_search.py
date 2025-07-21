"""
perplexity_search.py

PerplexitySearch: Integrate with Perplexity app for advanced web search.
"""
from typing import Optional
import pyperclip
from utils.keyboard_controller import KeyboardController

class PerplexitySearch:
    """Integrate with Perplexity app for advanced web search."""
    def __init__(self):
        self.perplexity_hotkey = ("ctrl", "shift", "p")
        self.keyboard = KeyboardController()

    def search(self, query: str) -> str:
        """Search using Perplexity app by simulating hotkey, typing, and copying result.

        Args:
            query (str): The search query.

        Returns:
            str: The extracted search result from Perplexity.
        """
        # Trigger Perplexity app
        self.keyboard.press_hotkey(*self.perplexity_hotkey)
        self.keyboard.wait(1.0)
        # Type the query and press Enter
        self.keyboard.type_text(query)
        self.keyboard.press_key('enter')
        self.keyboard.wait(5.0)  # Wait for Perplexity to generate response
        # Select all and copy
        self.keyboard.press_hotkey('ctrl', 'a')
        self.keyboard.press_hotkey('ctrl', 'c')
        self.keyboard.wait(0.5)
        # Get clipboard contents
        result = pyperclip.paste()
        return result or "[Perplexity search: No result copied from clipboard]" 