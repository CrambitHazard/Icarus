"""
confirm.py

Utility for safety confirmations before destructive actions.
"""

def confirm_action(prompt: str) -> bool:
    """Asks the user to confirm an action.

    Args:
        prompt (str): The confirmation prompt.

    Returns:
        bool: True if confirmed, False otherwise.
    """
    while True:
        ans = input(f"{prompt} [y/n]: ").strip().lower()
        if ans in ('y', 'yes'):
            return True
        if ans in ('n', 'no'):
            return False
        print("Please enter 'y' or 'n'.") 