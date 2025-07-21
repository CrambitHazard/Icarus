"""
system_tools.py

System tools for common queries: time, battery, date, etc.
"""
import datetime
import psutil

def get_current_time() -> str:
    """Returns the current system time as a string."""
    return datetime.datetime.now().strftime('%H:%M:%S')

def get_current_date() -> str:
    """Returns the current system date as a string."""
    return datetime.datetime.now().strftime('%Y-%m-%d')

def get_battery_percentage() -> str:
    """Returns the current battery percentage, or a message if not available."""
    try:
        battery = psutil.sensors_battery()
        if battery is not None:
            return f"Battery: {battery.percent}%"
        else:
            return "Battery information not available."
    except Exception:
        return "Battery information not available."

def get_cpu_usage() -> str:
    """Returns the current CPU usage percentage."""
    try:
        import psutil
        return f"CPU Usage: {psutil.cpu_percent()}%"
    except Exception:
        return "CPU usage information not available."

def get_ram_usage() -> str:
    """Returns the current RAM usage percentage."""
    try:
        import psutil
        mem = psutil.virtual_memory()
        return f"RAM Usage: {mem.percent}%"
    except Exception:
        return "RAM usage information not available."

def get_clipboard() -> str:
    """Returns the current clipboard contents."""
    try:
        import pyperclip
        return f"Clipboard: {pyperclip.paste()}"
    except Exception:
        return "Clipboard information not available."

def set_clipboard(text: str) -> str:
    """Sets the clipboard contents to the given text."""
    try:
        import pyperclip
        pyperclip.copy(text)
        return "Clipboard updated."
    except Exception:
        return "Failed to update clipboard."

def open_url(url: str) -> str:
    """Opens the given URL in the default web browser."""
    try:
        import webbrowser
        webbrowser.open(url)
        return f"Opened URL: {url}"
    except Exception:
        return "Failed to open URL."

def get_weather(location: str = "your area") -> str:
    """Returns a dummy weather report (real API integration can be added)."""
    return f"The weather in {location} is sunny and 25°C."

def get_random_joke() -> str:
    """Returns a random joke (dummy)."""
    return "Why did the computer go to the doctor? Because it had a virus!" 