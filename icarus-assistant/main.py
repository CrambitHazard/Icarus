"""
main.py

Main loop for Icarus Assistant MVP: STT → LLM → TTS + File reading.
"""

import os
import yaml
import json
import uuid
import signal
import sys
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
from utils.jarvis_responses import JarvisResponses

# TODO: Implement logging to data/logs/interaction_log.json

def check_tts_health(tts_instance):
    """Check if TTS is working and reinitialize if needed."""
    if not tts_instance.available:
        try:
            tts_instance.stop()
            new_tts = OpenVoiceTTS()
            if new_tts.available:
                return new_tts
        except Exception as e:
            print(f"[TTS] Failed to reinitialize TTS: {e}")
    return tts_instance

def test_tts(tts_instance):
    """Test TTS functionality with a simple message."""
    try:
        # Just test if TTS is available without speaking
        return tts_instance.available
    except Exception as e:
        print(f"[TTS] Test failed: {e}")
        return False


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
    help_text = JarvisResponses.style_response("""
Sir, here are my available capabilities:

VOICE COMMANDS:
- "Hello" / "Hi" - Greetings
- "Goodbye" / "Bye" - Farewell
- "What can you do?" - List capabilities

FILE OPERATIONS:
- "Search for <filename>" - Find files
- "Read <filename>" - Read file contents
- "List files" - Show directory contents
- "Edit <filename>" - Edit text files
- "Move <filename>" - Move files
- "Summarize <filename>" - Summarize PDFs

SYSTEM TOOLS:
- "System info" - System status
- "Launch <app>" - Start applications
- "What time is it?" - Current time
- "Battery status" - Battery level
- "CPU usage" - Processor status
- "RAM usage" - Memory status

VOICE SETTINGS:
- "Set voice to <name>" - Change TTS voice
- "Set speed to <number>" - Adjust speech rate
- "Mute TTS" / "Unmute TTS" - Toggle speech

MODE SWITCHING:
- "Manual" - Switch to text input
- "Voice" - Switch to voice input
- "Exit" - Close assistant

I'm ready to assist with any of these tasks, sir.
""")
    print(help_text)


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
    # Global TTS instance for cleanup
    global tts
    
    # Load config and initialize components
    config = load_config()
    memory_manager = MemoryManager()
    openrouter_client = OpenRouterClient(api_key=config['api_key'], model=config['model'])
    session_manager = SessionManager(memory_manager)
    intent_router = ContextAwareIntentRouter(memory_manager, openrouter_client)
    wakeword = WakewordListener()
    perplexity = PerplexitySearch()
    
    # Initialize STT and TTS
    stt = WhisperSTT()
    tts = OpenVoiceTTS()
    audio_handler = AudioHandler()
    
    # Set up signal handlers for clean shutdown
    def signal_handler(sig, frame):
        print(f"\nIcarus: {JarvisResponses.get_farewell()}")
        if tts:
            tts.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Icarus Assistant initialized. All systems operational.")
    print("Say 'Icarus' to activate or type 'manual' for manual input mode.")
    
    # Test TTS functionality
    if not test_tts(tts):
        print("[TTS] Warning: TTS may not be working properly")
    
    # Initial greeting
    initial_greeting = JarvisResponses.get_greeting()
    print(f"Icarus: {initial_greeting}")
    try:
        tts.speak_sync(initial_greeting)
    except Exception as tts_error:
        print(f"[TTS] Error in initial greeting: {tts_error}")
        # Try to reinitialize TTS
        try:
            tts.stop()
            tts = OpenVoiceTTS()
        except Exception as reinit_error:
            print(f"[TTS] Failed to reinitialize: {reinit_error}")
    session_id = None
    manual_mode = False
    tts_check_counter = 0
    
    while True:
        # Periodic TTS health check (every 10 iterations)
        tts_check_counter += 1
        if tts_check_counter >= 10:
            tts = check_tts_health(tts)
            tts_check_counter = 0
        try:
            if not manual_mode:
                # Wait for wake-word
                detected = wakeword.listen_for_wakeword(wakeword="icarus", feedback=False)
                if not detected:
                    continue
                print("Icarus: I'm listening, sir...")
                
                # Record audio and transcribe
                audio_file = audio_handler.record_audio(duration=5)  # Record for 5 seconds
                if audio_file:
                    user_input = stt.transcribe(audio_file)
                    print(f"You: {user_input}")
                else:
                    error_msg = JarvisResponses.get_error_response()
                    print(f"Icarus: {error_msg}")
                    continue
            else:
                # Manual input mode
                user_input = input("You (manual): ")
                if user_input.lower() == 'voice':
                    manual_mode = False
                    mode_message = JarvisResponses.style_response("I've switched to voice mode", "confirmation")
                    print(f"Icarus: {mode_message}")
                    continue
                elif user_input.lower() == 'exit':
                    break
            
            if user_input.lower() == 'manual':
                manual_mode = True
                mode_message = JarvisResponses.style_response("I've switched to manual mode", "confirmation")
                print(f"Icarus: {mode_message}")
                continue
            elif user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'help':
                show_help()
                continue
            
            if not session_id:
                session_id = str(uuid.uuid4())
                session_manager.create_session(session_id)
            
            memory_manager.store_message(session_id, 'user', user_input)
            
            # Route intent
            try:
                routed = intent_router.route_intent(user_input, session_id)
                
                for action, params in routed:
                    if action == 'greeting':
                        response = JarvisResponses.get_greeting()
                    elif action == 'farewell':
                        response = JarvisResponses.get_farewell()
                    elif action == 'plan_mode':
                        response = JarvisResponses.style_response(params.get('result', 'No result'))
                    elif action == 'perplexity_search':
                        response = JarvisResponses.style_response(params.get('result', 'No result'))
                    elif action == 'direct_response':
                        response = JarvisResponses.style_response(params.get('target', 'No response'))
                    elif action == 'tool_call':
                        response = JarvisResponses.style_response(f"I've executed {params.get('target', 'Unknown tool')}", "confirmation")
                    elif action == 'function_call':
                        response = JarvisResponses.style_response(f"I've executed {params.get('target', 'Unknown function')}", "confirmation")
                    elif action == 'llm_chat':
                        # Handle direct LLM chat
                        llm_response = openrouter_client.query(user_input)
                        response = JarvisResponses.style_response(llm_response)
                    else:
                        response = JarvisResponses.style_response("I've processed your request", "confirmation")
                    
                    print(f"Icarus: {response}")
                    memory_manager.store_message(session_id, 'assistant', response)
                    
                    # Speak response if not in manual mode
                    if not manual_mode:
                        try:
                            tts.speak_sync(response)
                        except Exception as tts_error:
                            print(f"[TTS] Error speaking response: {tts_error}")
                            # Try to reinitialize TTS
                            try:
                                tts.stop()
                                tts = OpenVoiceTTS()
                            except Exception as reinit_error:
                                print(f"[TTS] Failed to reinitialize: {reinit_error}")
                        
            except Exception as e:
                # Fallback to direct LLM response
                try:
                    llm_response = openrouter_client.query(user_input)
                    response = JarvisResponses.style_response(llm_response)
                    print(f"Icarus: {response}")
                    memory_manager.store_message(session_id, 'assistant', response)
                    if not manual_mode:
                        try:
                            tts.speak_sync(response)
                        except Exception as tts_error:
                            print(f"[TTS] Error speaking response: {tts_error}")
                except Exception as llm_error:
                    response = JarvisResponses.get_error_response()
                    print(f"Icarus: {response}")
                    memory_manager.store_message(session_id, 'assistant', response)
                    if not manual_mode:
                        try:
                            tts.speak_sync(response)
                        except Exception as tts_error:
                            print(f"[TTS] Error speaking response: {tts_error}")
                    
        except KeyboardInterrupt:
            print(f"\nIcarus: {JarvisResponses.get_farewell()}")
            # Clean up TTS
            tts.stop()
            break
        except Exception as e:
            error_msg = JarvisResponses.get_error_response()
            print(f"Icarus: {error_msg}")
            continue


if __name__ == "__main__":
    main()
