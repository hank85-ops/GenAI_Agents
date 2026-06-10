from chatbot.helpers import get_response

print("🤖 Banking Chatbot started! Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Bot: Goodbye! Have a great day!")
        break
    if not user_input:
        continue
    response = get_response(user_input)
    print(f"Bot: {response}\n")