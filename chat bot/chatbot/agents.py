import random
from chatbot.intents import intents


def get_response(user_input: str) -> str:
    """Get chatbot response based on user input"""
    user_input = user_input.lower().strip()
    for intent, data in intents.items():
        keywords = data.get("keywords", [])
        responses = data.get("response", [])
        for keyword in keywords:
            if keyword.lower() in user_input.split():
                if isinstance(responses, list):
                    return random.choice(responses)
                return responses
    return "Sorry, I didn't understand. Can you please rephrase?"