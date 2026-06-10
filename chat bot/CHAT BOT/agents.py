from chatbot.intents import intents
import random

def get_response(user_input):
    user_input = user_input.lower().strip()

    for intent, data in intents.items():
        keywords = data.get("keywords", [])
        responses = data.get("response", [])

        for keyword in keywords:
            # Match whole words instead of substring
            if keyword.lower() in user_input.split():
                if isinstance(responses, list):
                    return random.choice(responses)
                return responses  # If single response string

    return "Sorry, I didn’t understand. Can you please rephrase?"