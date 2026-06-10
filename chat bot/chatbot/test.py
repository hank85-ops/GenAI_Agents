from chatbot.helpers import get_response, debug_intent

test_inputs = [
    "What is my balance?",
    "I want to transfer money",
    "Tell me about loans",
    "I need a credit card",
    "I need help",
    "random unknown input"
]

print("Running chatbot tests...\n")
for user_input in test_inputs:
    print(f"User : {user_input}")
    print(f"Debug: {debug_intent(user_input)}")
    print(f"Bot  : {get_response(user_input)}")
    print("-" * 50)