"""
wakeword_listener.py

Wake-word detection for Icarus Assistant ("Icarus").
"""
import speech_recognition as sr
import pyaudio
import time
import difflib

class WakewordListener:
    """Detects the 'Icarus' wake-word using microphone input."""
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def listen_for_wakeword(self, wakeword="icarus", callback=None, phrase_time_limit=3, timeout=10, feedback=True):
        """Listens for the 'Icarus' wake-word or similar-sounding words. Blocks until detected or callback returns True.

        Args:
            wakeword (str): The wake-word to listen for.
            callback (callable, optional): Called on detection. If returns True, stops listening.
            phrase_time_limit (int): Max seconds per phrase.
            timeout (int): Max seconds to wait for wake-word before returning False.
            feedback (bool): If True, print/listen feedback.
        Returns:
            bool: True if wake-word detected, False if timeout.
        """
        similar_words = [wakeword,"jarvis", "jar wish", "acer", "acres", "ikarus", "icaros", "eicarus", "ikeros", "akers", "icurus", "ikeras"]
        if feedback:
            print(f"[WakewordListener] Say '{wakeword}' to activate. Listening...")
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            start = time.time()
            while True:
                if timeout and (time.time() - start) > timeout:
                    if feedback:
                        print(f"[WakewordListener] Timeout: No wake-word detected.")
                    return False
                try:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                    text = self.recognizer.recognize_google(audio).lower()
                    if feedback:
                        print(f"[WakewordListener] Heard: {text}")
                    # Fuzzy match: accept if any word in text is close to wakeword or similar
                    words = text.split()
                    for word in words:
                        matches = difflib.get_close_matches(word, similar_words, n=1, cutoff=0.7)
                        if matches:
                            if feedback:
                                print(f"[WakewordListener] Wake-word '{matches[0]}' detected! I'm listening...")
                            if callback:
                                if callback():
                                    return True
                            else:
                                return True
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    if feedback:
                        print(f"[WakewordListener] Error: {e}")
                    continue 