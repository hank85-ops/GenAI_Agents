import re
import random
from chatbot.intents import intents


def clean_input(user_input: str) -> str:
    """Normalize user input (lowercase + strip spaces)"""
    return user_input.lower().strip()


def match_intent(user_input: str):
    """Match user input with intent using keyword search"""
    for intent_name, data in intents.items():
        keywords = data.get("keywords", [])
        for keyword in keywords:
            pattern = rf"\b{re.escape(keyword.lower())}\b"
            if re.search(pattern, user_input):
                return intent_name, data
    return None, None


def get_response(user_input: str) -> str:
    """Main function to get chatbot response"""
    if not user_input or not user_input.strip():       # ← fix: guard empty input
        return "Please type a message."

    user_input = clean_input(user_input)
    intent_name, data = match_intent(user_input)

    if intent_name and data:                           # ← fix: check both not None
        responses = data.get("response", [])
        if not responses:                              # ← fix: guard empty responses
            return "Sorry, no response available."
        if isinstance(responses, list):
            return random.choice(responses)
        return responses

    return "Sorry, I didn't understand. Can you please rephrase?"


def debug_intent(user_input: str) -> str:             # ← fix: always returns str
    """Debug function to check matched intent"""
    if not user_input or not user_input.strip():
        return "No input provided"

    user_input = clean_input(user_input)
    intent_name, _ = match_intent(user_input)

    if intent_name:
        return f"Matched Intent: {intent_name}"
    return "No intent matched"                        # ← fix: was returning None