"""
keyboard_controller.py

KeyboardController: Control keyboard for app interactions (Perplexity, etc.).
"""
import pyautogui
import time

class KeyboardController:
    """Control keyboard for app interactions using pyautogui."""
    def __init__(self):
        pass

    def press_hotkey(self, *keys):
        """Press a combination of keys.

        Args:
            *keys: Variable length key arguments (e.g., 'ctrl', 'shift', 'p').
        """
        pyautogui.hotkey(*keys)

    def type_text(self, text: str, delay: float = 0.1):
        """Type text with optional delay between keystrokes.

        Args:
            text (str): Text to type.
            delay (float): Delay between keystrokes in seconds.
        """
        pyautogui.write(text, interval=delay)

    def press_key(self, key: str):
        """Press a single key.

        Args:
            key (str): Key to press.
        """
        pyautogui.press(key)

    def wait(self, seconds: float):
        """Wait for specified time.

        Args:
            seconds (float): Time to wait in seconds.
        """
        time.sleep(seconds) 