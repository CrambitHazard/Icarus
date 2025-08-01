"""
openvoice_wrapper.py

Text-to-Speech (TTS) wrapper for OpenVoice (manual setup required). Falls back to pyttsx3 for local TTS.
"""

import threading
import time
import queue
from typing import Optional

class OpenVoiceTTS:
    """Wrapper for OpenVoice TTS. Falls back to pyttsx3 if OpenVoice is not available.

    Methods:
        speak(text: str) -> None: Speaks the given text aloud.
        set_voice(voice_name: str) -> None: Sets the TTS voice.
        set_speed(rate: int) -> None: Sets the TTS speech rate.
        set_volume(volume: float) -> None: Sets the TTS volume (0.0 to 1.0).
        mute() -> None: Mutes TTS output.
        unmute() -> None: Unmutes TTS output.
    """
    def __init__(self):
        """Initializes the OpenVoice TTS system or fallback TTS."""
        self.available = False
        self.muted = False
        self.engine = None
        self.speech_queue = queue.Queue()
        self.tts_thread = None
        self.should_stop = False
        
        # Initialize TTS engine
        self._init_tts_engine()
        
        # Start TTS thread if available
        if self.available:
            self._start_tts_thread()

    def _init_tts_engine(self):
        """Initialize the TTS engine with error handling."""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            
            # Test the engine
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 0.8)
            
            # Get available voices
            voices = self.engine.getProperty('voices')
            if voices:
                # Set a default voice
                self.engine.setProperty('voice', voices[0].id)
            
            self.available = True
            print("[TTS] Engine initialized successfully")
            
        except Exception as e:
            print(f"[TTS] Failed to initialize TTS engine: {e}")
            self.available = False
            self.engine = None

    def _start_tts_thread(self):
        """Start the TTS worker thread."""
        if self.tts_thread is None or not self.tts_thread.is_alive():
            self.should_stop = False
            self.tts_thread = threading.Thread(target=self._tts_worker, daemon=True)
            self.tts_thread.start()
            print("[TTS] TTS thread started")

    def _tts_worker(self):
        """Worker thread for handling TTS requests."""
        while not self.should_stop:
            try:
                # Get text from queue with timeout
                text = self.speech_queue.get(timeout=1.0)
                
                if text is None:  # Shutdown signal
                    break
                    
                if not self.muted and self.available and self.engine:
                    self._speak_text(text)
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"[TTS] Error in TTS worker: {e}")
                # Try to reinitialize engine
                self._reinit_engine()
                
        print("[TTS] TTS worker thread stopped")

    def _speak_text(self, text: str):
        """Actually speak the text with error handling."""
        try:
            if self.engine:
                self.engine.say(text)
                self.engine.runAndWait()
        except Exception as e:
            print(f"[TTS] Error speaking text: {e}")
            # Try to reinitialize engine
            self._reinit_engine()

    def _reinit_engine(self):
        """Reinitialize the TTS engine if it fails."""
        try:
            if self.engine:
                self.engine.stop()
        except:
            pass
        
        time.sleep(0.5)  # Brief pause
        self._init_tts_engine()

    def speak(self, text: str) -> None:
        """Speaks the given text aloud, unless muted.

        Args:
            text (str): The text to speak.
        """
        if not text or not text.strip():
            return
            
        if self.muted:
            print("[TTS] Muted. No speech output.")
            return
            
        if not self.available:
            print("[TTS] TTS not available.")
            return
            
        try:
            # Add text to queue for async processing
            self.speech_queue.put(text.strip())
        except Exception as e:
            print(f"[TTS] Error queuing speech: {e}")

    def speak_sync(self, text: str) -> None:
        """Speaks text synchronously (blocking) for immediate feedback."""
        if not text or not text.strip() or self.muted:
            return
            
        if not self.available:
            print("[TTS] TTS not available.")
            return
            
        try:
            self._speak_text(text.strip())
        except Exception as e:
            print(f"[TTS] Error in sync speech: {e}")

    def set_voice(self, voice_name: str) -> None:
        """Sets the TTS voice and provides spoken feedback."""
        if not self.available or not self.engine:
            print("[TTS] TTS not available.")
            return
            
        try:
            voices = self.engine.getProperty('voices')
            for v in voices:
                if voice_name.lower() in v.name.lower() or voice_name.lower() in v.id.lower():
                    self.engine.setProperty('voice', v.id)
                    print(f"[TTS] Voice set to: {v.name}")
                    self.speak_sync(f"Voice set to {voice_name}.")
                    return
            print(f"[TTS] Voice '{voice_name}' not found. Available: {[v.name for v in voices]}")
        except Exception as e:
            print(f"[TTS] Error setting voice: {e}")

    def set_speed(self, rate: int) -> None:
        """Sets the TTS speech rate and provides spoken feedback."""
        if not self.available or not self.engine:
            print("[TTS] TTS not available.")
            return
            
        try:
            # Clamp rate to reasonable values
            rate = max(50, min(300, rate))
            self.engine.setProperty('rate', rate)
            print(f"[TTS] Rate set to: {rate}")
            self.speak_sync(f"Speed set to {rate}.")
        except Exception as e:
            print(f"[TTS] Error setting speed: {e}")

    def set_volume(self, volume: float) -> None:
        """Sets the TTS volume and provides spoken feedback."""
        if not self.available or not self.engine:
            print("[TTS] TTS not available.")
            return
            
        try:
            # Clamp volume to 0.0-1.0
            volume = max(0.0, min(1.0, volume))
            self.engine.setProperty('volume', volume)
            print(f"[TTS] Volume set to: {volume}")
            self.speak_sync(f"Volume set to {volume}.")
        except Exception as e:
            print(f"[TTS] Error setting volume: {e}")

    def mute(self) -> None:
        """Mutes TTS output and provides feedback."""
        self.muted = True
        print("[TTS] Muted.")
        self.speak_sync("TTS muted.")

    def unmute(self) -> None:
        """Unmutes TTS output and provides feedback."""
        self.muted = False
        print("[TTS] Unmuted.")
        self.speak_sync("TTS unmuted.")

    def stop(self):
        """Stop the TTS system and clean up."""
        self.should_stop = True
        if self.speech_queue:
            self.speech_queue.put(None)  # Signal shutdown
        if self.tts_thread and self.tts_thread.is_alive():
            self.tts_thread.join(timeout=2.0)
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
        print("[TTS] TTS system stopped")

    def __del__(self):
        """Cleanup when object is destroyed."""
        self.stop()
