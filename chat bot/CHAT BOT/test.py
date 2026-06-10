import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from CHATBOT.helpers import get_response

print("CHAT BOT started...")

while True:
    user = input("You: ")
    if user.lower() == "exit":
        break

    print("Bot:", get_response(user))
