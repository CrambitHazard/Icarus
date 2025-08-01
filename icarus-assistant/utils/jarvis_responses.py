"""
jarvis_responses.py

Jarvis-style response templates for Icarus Assistant.
"""

import random
from datetime import datetime

class JarvisResponses:
    """Jarvis-style response templates and utilities."""
    
    @staticmethod
    def get_greeting() -> str:
        """Get a Jarvis-style greeting based on time of day."""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            time_greeting = "Good morning"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= hour < 22:
            time_greeting = "Good evening"
        else:
            time_greeting = "Good evening"
        
        greetings = [
            f"{time_greeting}, sir. Icarus at your service.",
            f"{time_greeting}. How may I assist you today?",
            f"{time_greeting}. All systems are operational and ready for your commands.",
            f"{time_greeting}. I'm listening.",
            f"{time_greeting}. What can I do for you?"
        ]
        
        return random.choice(greetings)
    
    @staticmethod
    def get_farewell() -> str:
        """Get a Jarvis-style farewell."""
        farewells = [
            "Goodbye, sir. I'll be here when you need me.",
            "Farewell. All systems will remain on standby.",
            "Until next time. Icarus signing off.",
            "Goodbye. Don't hesitate to call if you need assistance.",
            "See you later, sir. I'll keep everything running smoothly."
        ]
        
        return random.choice(farewells)
    
    @staticmethod
    def get_system_status() -> str:
        """Get a Jarvis-style system status report."""
        return "All systems are functioning normally, sir. I'm ready to assist with any task you require."
    
    @staticmethod
    def get_confirmation() -> str:
        """Get a Jarvis-style confirmation."""
        confirmations = [
            "Understood, sir.",
            "Affirmative.",
            "Consider it done.",
            "I'll handle that for you.",
            "Processing your request."
        ]
        
        return random.choice(confirmations)
    
    @staticmethod
    def get_error_response() -> str:
        """Get a Jarvis-style error response."""
        error_responses = [
            "I apologize, sir. There seems to be a technical difficulty.",
            "I'm experiencing some issues with that request. Please try again.",
            "I'm afraid I'm unable to process that at the moment.",
            "There appears to be a problem with that operation.",
            "I'm encountering some difficulties. Let me try a different approach."
        ]
        
        return random.choice(error_responses)
    
    @staticmethod
    def get_thinking_response() -> str:
        """Get a Jarvis-style thinking response."""
        thinking_responses = [
            "Processing your request, sir.",
            "Analyzing the situation.",
            "Let me work on that for you.",
            "I'm on it.",
            "Working on your request."
        ]
        
        return random.choice(thinking_responses)
    
    @staticmethod
    def style_response(response: str, context: str = "general") -> str:
        """Style a response to be more Jarvis-like."""
        if context == "greeting":
            return JarvisResponses.get_greeting()
        elif context == "farewell":
            return JarvisResponses.get_farewell()
        elif context == "error":
            return JarvisResponses.get_error_response()
        elif context == "confirmation":
            return JarvisResponses.get_confirmation()
        elif context == "thinking":
            return JarvisResponses.get_thinking_response()
        else:
            # For ALL responses, add Jarvis-style prefixes consistently
            prefixes = [
                "Sir, ",
                "I should mention that ",
                "I've found that ",
                "According to my analysis, ",
                "I can tell you that ",
                "Based on my assessment, ",
                "I should note that ",
                "I've discovered that ",
                "From what I can see, ",
                "I believe that ",
                "I can confirm that ",
                "I've determined that ",
                "I should point out that ",
                "I've observed that ",
                "I can assure you that ",
                ""
            ]
            
            # Always add a prefix for consistency (80% chance)
            if random.random() < 0.8:
                prefix = random.choice(prefixes)
                styled_response = f"{prefix}{response}"
            else:
                styled_response = response
            
            # Add Jarvis-style suffixes occasionally (30% chance)
            suffixes = [
                ", sir.",
                ", if you need anything else.",
                ". Is there anything else I can assist you with?",
                ". I'm here if you need me.",
                ". Let me know if you require further assistance.",
                ". I'm ready for your next command.",
                ". How else may I be of service?",
                ". I'm at your disposal.",
                ". I'm listening for your next request.",
                ". I'm here to help.",
                ""
            ]
            
            if random.random() < 0.3:
                suffix = random.choice(suffixes)
                return f"{styled_response}{suffix}"
            else:
                return styled_response 