"""
main.py

Main loop for Icarus Assistant MVP: STT → LLM → TTS + File reading.
"""

import os
import yaml
import json
from stt.whisper_wrapper import WhisperSTT
from llm.openrouter_client import OpenRouterClient
from tts.openvoice_wrapper import OpenVoiceTTS
from utils.audio_handler import AudioHandler
from actions.read_file import read_file
from dotenv import load_dotenv
from orchestrator.intent_router import route_intent, ContextAwareIntentRouter
from actions.search_files import search_files, present_file_matches, list_files_in_directory, get_system_info
from actions.launch_app import launch_app, update_app_map, get_app_names, get_app_map
from utils.confirm import confirm_action
from utils.path_guard import is_safe_path
from datetime import datetime
from orchestrator.wakeword_listener import WakewordListener
from orchestrator.memory_manager import MemoryManager
from orchestrator.conversation_graph import ConversationGraph
from llm.langchain_integration import LangChainLLM
from actions.system_tools import get_current_time, get_current_date, get_battery_percentage, get_cpu_usage, get_ram_usage, get_clipboard, set_clipboard, open_url, get_weather, get_random_joke
from actions.edit_text import edit_text
from actions.move_files import move_file
from actions.summarize_pdf import summarize_pdf
from orchestrator.llm_brain import LLMBrain
from orchestrator.plan_executor import PlanExecutor
from actions.perplexity_search import PerplexitySearch
from orchestrator.session_manager import SessionManager

# TODO: Implement logging to data/logs/interaction_log.json


def load_config():
    """Loads OpenRouter config from .env.local or config/openrouter.yaml.

    Returns:
        dict: Config dictionary with API key and model.
    """
    # Load .env.local if present
    load_dotenv(dotenv_path='.env.local')
    api_key = os.getenv('OPENROUTER_API_KEY')
    model = None
    if api_key:
        # Optionally load model from YAML if present
        config_path = os.path.join('config', 'openrouter.yaml')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                model = config.get('model', 'default-model')
        else:
            model = 'default-model'
        return {'api_key': api_key, 'model': model}
    # Fallback to YAML config
    config_path = os.path.join('config', 'openrouter.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def log_interaction(user_text: str, response: str):
    """Logs the interaction to data/logs/interaction_log.json.

    Args:
        user_text (str): User's input text.
        response (str): Assistant's response.
    """
    log_path = os.path.join('data', 'logs', 'interaction_log.json')
    entry = {
        'user': user_text,
        'response': response,
        'timestamp': datetime.now().isoformat(),
    }
    # Append to log file
    try:
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(entry)
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"Error logging interaction: {e}")


def show_help():
    print("""
Icarus Assistant Commands:
- help: Show this help message
- exit: Exit the assistant
- voice: Switch to voice mode
- manual: Switch to manual mode
- repeat: Repeat last response
- clear log: Clear the interaction log
- show log: Show the interaction log
- search for <name>: Search for files
- read <file>: Read a file aloud
- launch <app>: Launch an application
- list files: List files in a directory
- set voice to <name>: Set TTS voice
- set speed to <num>: Set TTS speed
- set volume to <num>: Set TTS volume
- mute/unmute tts: Mute or unmute TTS
- transcribe only: Switch to transcription-only mode
- add/map app <name> as/to <path>: Add or update app launch mapping
- system info/list running apps/show processes: Show system/process info
- edit/move/delete <file>: Edit, move, or delete a file (with confirmation)
- (and more: edit, move, system tools coming soon)
""")


def clear_log():
    log_path = os.path.join('data', 'logs', 'interaction_log.json')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('[]')
    print("[Log] Interaction log cleared.")


def show_log():
    log_path = os.path.join('data', 'logs', 'interaction_log.json')
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        print("[Log] Interaction log:")
        for entry in logs:
            print(f"User: {entry['user']}\nIcarus: {entry['response']}\n---")
    except Exception as e:
        print(f"[Log] Error reading log: {e}")


def llm_disambiguate_apps(user_query: str, app_map: dict, llm) -> list:
    """Use LLM to parse user query and return a list of app names to launch from the app map. Prefer a single best match."""
    prompt = (
        "You are an assistant that helps launch applications on a user's computer. "
        "Given the user's request and the following list of available apps, "
        "return the single best app name (from the list) that best matches the user's intent. "
        "If the user clearly wants more than one, return a comma-separated list, but prefer only one.\n"
        f"Available apps: {', '.join(app_map.keys())}\n"
        f"User request: {user_query}\n"
        "Apps to launch (comma-separated, use only names from the list):"
    )
    response = llm.query(prompt)
    # Parse comma-separated app names
    return [name.strip() for name in response.split(',') if name.strip() in app_map]


def main():
    """Main loop for Icarus Assistant Phase 3: persistent, context-aware, hands-free."""
    # Load config and initialize components
    memory_manager = MemoryManager()
    openrouter_client = OpenRouterClient(api_key='${OPENROUTER_API_KEY}', model='gpt-4')
    session_manager = SessionManager(memory_manager)
    intent_router = ContextAwareIntentRouter(memory_manager, openrouter_client)
    wakeword = WakewordListener()
    perplexity = PerplexitySearch()
    # ... (initialize TTS, STT, etc.)

    print("[Persistent Mode] Say 'Icarus' to activate.")
    session_id = None
    while True:
        try:
            # Wait for wake-word
            detected = wakeword.listen_for_wakeword(wakeword="icarus", feedback=True)
            if not detected:
                print("[Persistent Mode] No wake-word detected. Waiting again...")
                continue
            print("[Persistent Mode] Listening for your command...")
            # Record and transcribe audio (stub)
            user_input = input("You (simulated STT): ")
            if not session_id:
                session_id = str(uuid.uuid4())
                session_manager.create_session(session_id)
            memory_manager.store_message(session_id, 'user', user_input)
            # Route intent
            routed = intent_router.route_intent(user_input, session_id)
            for action, params in routed:
                if action == 'plan_mode':
                    print(f"[Plan Mode] {params['result']}")
                elif action == 'perplexity_search':
                    print(f"[Perplexity] {params['result']}")
                elif action == 'direct_response':
                    print(f"[Assistant] {params.get('target')}")
                elif action == 'tool_call':
                    print(f"[Tool] {params.get('target')} with {params.get('parameters')}")
                elif action == 'function_call':
                    print(f"[Function] {params.get('target')} with {params.get('parameters')}")
                else:
                    print(f"[Other] {params}")
                memory_manager.store_message(session_id, 'assistant', str(params))
        except KeyboardInterrupt:
            print("\nExiting Icarus Assistant.")
            break
        except Exception as e:
            print(f"[Error] {e}")
            continue


if __name__ == "__main__":
    main()
