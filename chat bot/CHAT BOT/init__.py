from CHATBOT.intents import intents

def get_response(user_input):
    user_input = user_input.lower()

    for intent, data in intents.items():
        for keyword in data["keywords"]:
            if keyword in user_input:
                return data["response"]

    return "Sorry, I didn’t understand. Can you please rephrase?"