"""
intent_router.py

Determines user intent and routes to the appropriate tool or LLM.
"""

from typing import Tuple, List
from orchestrator.llm_brain import LLMBrain
from orchestrator.plan_executor import PlanExecutor
from actions.perplexity_search import PerplexitySearch
from orchestrator.session_manager import SessionManager

def route_intent(user_input: str) -> List[Tuple[str, dict]]:
    """Determines the user's intent(s) and returns a list of (intent, parameters) for each command.

    Args:
        user_input (str): The user's input text.

    Returns:
        List[Tuple[str, dict]]: List of (intent, parameters) pairs.
    """
    # Split input on ' and ' for multi-command support
    parts = [p.strip() for p in user_input.lower().split(' and ') if p.strip()]
    results = []
    last_verb = None
    for i, text in enumerate(parts):
        # Detect verb for this part
        verb = None
        if any(k in text for k in ['launch', 'open app', 'start app', 'run app']) or text.startswith('open '):
            verb = 'launch_app'
        elif any(k in text for k in ['list files', 'show files', 'files in', 'what files']):
            verb = 'list_files'
        elif any(k in text for k in ['search for', 'find file', 'look for', 'search file']):
            verb = 'search_files'
        elif text.startswith('read') or 'read' in text:
            verb = 'read_file'
        elif any(k in text for k in ['edit', 'change', 'modify']):
            verb = 'edit_text'
        elif any(k in text for k in ['move', 'copy', 'relocate']):
            verb = 'move_files'
        elif any(k in text for k in ['delete', 'remove', 'erase']):
            verb = 'delete_file'
        elif any(k in text for k in ['system info', 'list running apps', 'show processes', 'cpu', 'memory']):
            verb = 'system_info'
        elif any(k in text for k in ['mute tts', 'mute voice', 'mute speech']):
            verb = 'tts_mute'
        elif any(k in text for k in ['unmute tts', 'unmute voice', 'unmute speech']):
            verb = 'tts_unmute'
        elif 'set voice' in text:
            verb = 'tts_set_voice'
        elif 'set speed' in text or 'set rate' in text:
            verb = 'tts_set_speed'
        elif 'set volume' in text:
            verb = 'tts_set_volume'
        elif 'add app' in text or 'map app' in text:
            verb = 'update_app_map'
        elif any(k in text for k in ['what time', 'current time', 'time is it']):
            verb = 'system_time'
        elif any(k in text for k in ['what date', 'current date', 'date is it', 'today']):
            verb = 'system_date'
        elif any(k in text for k in ['battery', 'battery percentage', 'battery level']):
            verb = 'system_battery'
        elif any(k in text for k in ['cpu usage', 'cpu percent', 'processor usage']):
            verb = 'system_cpu'
        elif any(k in text for k in ['ram usage', 'memory usage', 'ram percent']):
            verb = 'system_ram'
        elif any(k in text for k in ['clipboard', 'get clipboard', 'show clipboard']):
            verb = 'system_clipboard_get'
        elif text.startswith('set clipboard to '):
            verb = 'system_clipboard_set'
        elif text.startswith('open url ') or text.startswith('go to '):
            verb = 'system_open_url'
        elif any(k in text for k in ['weather', 'forecast']):
            verb = 'system_weather'
        elif any(k in text for k in ['joke', 'make me laugh']):
            verb = 'system_joke'
        elif any(k in text for k in ['summarize pdf', 'summarize this pdf', 'summarize file']) or text.startswith('summarize'):
            verb = 'summarize_pdf'
        # Propagate previous verb if missing
        if not verb and last_verb:
            verb = last_verb
        if verb:
            last_verb = verb
        # Now handle as before, using verb
        if verb == 'list_files':
            import re
            match = re.search(r'(?:in|from)\s+([\w\\/\.-]+)', text)
            directory = match.group(1) if match else '.'
            results.append(('list_files', {'directory': directory}))
            continue
        if verb == 'search_files':
            results.append(('search_files', {'query': text}))
            continue
        if verb == 'read_file':
            results.append(('read_file', {'query': text}))
            continue
        if verb == 'edit_text':
            # Example: 'edit line 3 in file.txt to Hello world'
            import re
            match = re.search(r'edit(?: line (\d+))? in ([^ ]+) to (.+)', text)
            if match:
                line = int(match.group(1)) if match.group(1) else None
                fname = match.group(2)
                content = match.group(3)
                results.append(('edit_text', {'file': fname, 'operation': 'replace', 'content': content, 'line': line}))
            else:
                results.append(('edit_text', {'query': text, 'needs_confirmation': True}))
            continue
        if verb == 'move_files':
            # Example: 'move file.txt to folder/'
            import re
            match = re.search(r'move ([^ ]+) to ([^ ]+)', text)
            if match:
                src = match.group(1)
                dst = match.group(2)
                results.append(('move_files', {'src': src, 'dst': dst, 'copy': False, 'needs_confirmation': True}))
            else:
                results.append(('move_files', {'query': text, 'needs_confirmation': True}))
            continue
        if verb == 'delete_file':
            results.append(('delete_file', {'query': text, 'needs_confirmation': True}))
            continue
        if verb == 'launch_app':
            results.append(('launch_app', {'query': text}))
            continue
        if verb == 'system_info':
            results.append(('system_info', {}))
            continue
        if verb == 'tts_mute':
            results.append(('tts_mute', {}))
            continue
        if verb == 'tts_unmute':
            results.append(('tts_unmute', {}))
            continue
        if verb == 'tts_set_voice':
            import re
            match = re.search(r'set voice to ([\w\s-]+)', text)
            voice = match.group(1).strip() if match else ''
            results.append(('tts_set_voice', {'voice': voice}))
            continue
        if verb == 'tts_set_speed':
            import re
            match = re.search(r'(?:set speed|set rate) to (\d+)', text)
            speed = int(match.group(1)) if match else 200
            results.append(('tts_set_speed', {'speed': speed}))
            continue
        if verb == 'tts_set_volume':
            import re
            match = re.search(r'set volume to ([0-9.]+)', text)
            volume_str = match.group(1) if match else '1.0'
            # Strip trailing punctuation
            import string
            volume_str = volume_str.rstrip(string.punctuation)
            try:
                volume = float(volume_str)
            except Exception:
                volume = 1.0
            results.append(('tts_set_volume', {'volume': volume}))
            continue
        if verb == 'update_app_map':
            import re
            match = re.search(r'(?:add|map) app ([\w\s-]+) (?:as|to) ([\w\\/\.-]+)', text)
            if match:
                app_name = match.group(1).strip()
                path = match.group(2).strip()
                results.append(('update_app_map', {'app_name': app_name, 'path': path}))
                continue
        if verb == 'system_time':
            results.append(('system_time', {}))
            continue
        if verb == 'system_date':
            results.append(('system_date', {}))
            continue
        if verb == 'system_battery':
            results.append(('system_battery', {}))
            continue
        if verb == 'system_cpu':
            results.append(('system_cpu', {}))
            continue
        if verb == 'system_ram':
            results.append(('system_ram', {}))
            continue
        if verb == 'system_clipboard_get':
            results.append(('system_clipboard_get', {}))
            continue
        if verb == 'system_clipboard_set':
            import re
            match = re.search(r'set clipboard to (.+)', text)
            value = match.group(1) if match else ''
            results.append(('system_clipboard_set', {'value': value}))
            continue
        if verb == 'system_open_url':
            import re
            match = re.search(r'(?:open url|go to) (.+)', text)
            url = match.group(1) if match else ''
            results.append(('system_open_url', {'url': url}))
            continue
        if verb == 'system_weather':
            import re
            match = re.search(r'weather in ([\w\s]+)', text)
            location = match.group(1).strip() if match else 'your area'
            results.append(('system_weather', {'location': location}))
            continue
        if verb == 'system_joke':
            results.append(('system_joke', {}))
            continue
        if verb == 'summarize_pdf':
            # Example: 'summarize file.pdf'
            import re
            match = re.search(r'summarize ([^ ]+\.pdf)', text)
            if match:
                fname = match.group(1)
                results.append(('summarize_pdf', {'file': fname}))
            else:
                results.append(('summarize_pdf', {'query': text}))
            continue
        # Default: LLM chat
        results.append(('llm_chat', {'query': text}))
    return results 

class ContextAwareIntentRouter:
    """Routes user input to the correct tool/function using LLMBrain."""
    def __init__(self, memory_manager, openrouter_client):
        self.memory = memory_manager
        self.llm_brain = LLMBrain(openrouter_client, memory_manager)
        self.plan_executor = PlanExecutor(self.llm_brain, openrouter_client)
        self.perplexity = PerplexitySearch()
        self.session_manager = SessionManager(memory_manager)

    def route_intent(self, user_input: str, session_id: str) -> list:
        """Route user input using LLMBrain. Handles plan_mode and Perplexity search."""
        intent_struct = self.llm_brain.parse_intent(user_input, session_id)
        action = intent_struct.get('action')
        if action == 'plan_mode':
            plan_result = self.plan_executor.create_and_execute_plan(user_input, session_id)
            return [('plan_mode', {'result': plan_result})]
        elif action == 'tool_call' and intent_struct.get('target') == 'perplexity_search':
            result = self.perplexity.search(intent_struct['parameters'].get('query', user_input))
            return [('perplexity_search', {'result': result})]
        else:
            return [(action, intent_struct)] 