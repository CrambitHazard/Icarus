"""
openvoice_wrapper.py

Text-to-Speech (TTS) wrapper for OpenVoice (manual setup required). Falls back to pyttsx3 for local TTS.
"""

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
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            self.available = True
            self.muted = False
        except Exception:
            self.engine = None
            self.available = False
            self.muted = False

    def speak(self, text: str) -> None:
        """Speaks the given text aloud, unless muted.

        Args:
            text (str): The text to speak.
        """
        if self.muted:
            print("[TTS] Muted. No speech output.")
            return
        try:
            if self.available and self.engine:
                self.engine.say(text)
                self.engine.runAndWait()
            else:
                print("[TTS fallback] pyttsx3 not available. Please install pyttsx3 for local TTS.")
        except Exception as e:
            print(f"Error in TTS: {e}")
            raise

    def set_voice(self, voice_name: str) -> None:
        """Sets the TTS voice and provides spoken feedback."""
        if self.available and self.engine:
            voices = self.engine.getProperty('voices')
            for v in voices:
                if voice_name.lower() in v.name.lower() or voice_name.lower() in v.id.lower():
                    self.engine.setProperty('voice', v.id)
                    print(f"[TTS] Voice set to: {v.name}")
                    print(f"[TTS] Voice set to {voice_name}.")
                    self.speak(f"Voice set to {voice_name}.")
                    return
            print(f"[TTS] Voice '{voice_name}' not found. Available: {[v.name for v in voices]}")

    def set_speed(self, rate: int) -> None:
        """Sets the TTS speech rate and provides spoken feedback."""
        if self.available and self.engine:
            self.engine.setProperty('rate', rate)
            print(f"[TTS] Rate set to: {rate}")
            print(f"[TTS] Speed set to {rate}.")
            self.speak(f"Speed set to {rate}.")

    def set_volume(self, volume: float) -> None:
        """Sets the TTS volume and provides spoken feedback."""
        if self.available and self.engine:
            self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
            print(f"[TTS] Volume set to: {volume}")
            print(f"[TTS] Volume set to {volume}.")
            self.speak(f"Volume set to {volume}.")

    def mute(self) -> None:
        """Mutes TTS output and provides feedback."""
        self.muted = True
        print("[TTS] Muted.")
        self.speak("TTS muted.")

    def unmute(self) -> None:
        """Unmutes TTS output and provides feedback."""
        self.muted = False
        print("[TTS] Unmuted.")
        self.speak("TTS unmuted.")
