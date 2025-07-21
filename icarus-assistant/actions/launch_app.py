"""
launch_app.py

Launches applications by name or path.
"""

import os
import subprocess
import yaml
import difflib

def load_app_map() -> dict:
    """Loads the app launch map from config/app_map.yaml if present, else returns default map.

    Returns:
        dict: App name to executable/path mapping.
    """
    config_path = os.path.join('config', 'app_map.yaml')
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"[AppMap] Error loading app_map.yaml: {e}")
    # Default map
    return {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'chrome': 'chrome.exe',
        'explorer': 'explorer.exe',
        'cmd': 'cmd.exe',
        'powershell': 'powershell.exe',
    }

def update_app_map(app_name: str, path: str) -> str:
    """Updates the app_map.yaml with a new or updated app mapping.

    Args:
        app_name (str): Name of the app.
        path (str): Executable or path.
    Returns:
        str: Status message.
    """
    config_path = os.path.join('config', 'app_map.yaml')
    app_map = load_app_map()
    app_map[app_name.lower()] = path
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(app_map, f)
        return f"App '{app_name}' mapped to '{path}'."
    except Exception as e:
        return f"Failed to update app map: {e}"

def launch_app(app_query: str) -> str:
    """Launches an application by name or path. Loads user-editable app map from config/app_map.yaml. Uses fuzzy matching for app names.

    Args:
        app_query (str): The app name or path.

    Returns:
        str: Status message.
    """
    app_map = load_app_map()
    app = app_query.lower().strip()
    # Fuzzy match if no exact match
    app_names = list(app_map.keys())
    # Try exact match first
    for k, v in app_map.items():
        if k in app:
            try:
                os.startfile(v)
                return f"Launched {k}"
            except Exception as e:
                return f"Failed to launch {k}: {e}"
    # Fuzzy match
    close_matches = difflib.get_close_matches(app, app_names, n=1, cutoff=0.6)
    if close_matches:
        k = close_matches[0]
        v = app_map[k]
        try:
            os.startfile(v)
            return f"Launched {k} (fuzzy match for '{app_query}')"
        except Exception as e:
            return f"Failed to launch {k} (fuzzy match for '{app_query}'): {e}"
    # Try launching by path
    try:
        os.startfile(app_query)
        return f"Launched {app_query}"
    except Exception as e:
        return f"App '{app_query}' not found in app map and failed to launch by path: {e}"

def get_app_names() -> list:
    """Returns a list of all app names in the app map."""
    return list(load_app_map().keys())

def get_app_map() -> dict:
    """Returns the app map (name to path)."""
    return load_app_map() 