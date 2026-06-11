from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
from chatbot.helpers import get_response
import threading
import time
import random
import json
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'nexabank-secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# ── MOCK DATA ──────────────────────────────────────────
account = {
    "balance": 25000.00,
    "savings": 12500.00,
    "transactions": [
        {"id": 1, "desc": "Salary Credit",       "amount": +50000, "date": "10 Jun"},
        {"id": 2, "desc": "Amazon Purchase",      "amount":  -1200, "date": "09 Jun"},
        {"id": 3, "desc": "Electricity Bill",     "amount":   -850, "date": "08 Jun"},
        {"id": 4, "desc": "Netflix Subscription", "amount":   -199, "date": "07 Jun"},
        {"id": 5, "desc": "UPI Transfer",         "amount":  -3000, "date": "06 Jun"},
    ]
}

stocks = {
    "RELIANCE": {"price": 2845.50, "change": +1.2},
    "TCS":      {"price": 3920.00, "change": -0.4},
    "HDFC":     {"price": 1650.75, "change": +0.8},
    "INFY":     {"price": 1425.30, "change": -0.2},
    "SBIN":     {"price":  625.80, "change": +2.1},
}

forex = {
    "USD/INR": 83.45,
    "EUR/INR": 90.12,
    "GBP/INR": 105.67,
    "JPY/INR":  0.54,
    "AED/INR": 22.71,
}

# ── LIVE DATA SIMULATOR ────────────────────────────────
def simulate_live_data():
    while True:
        time.sleep(3)
        # Fluctuate stocks
        for sym in stocks:
            change_pct = random.uniform(-0.5, 0.5)
            stocks[sym]["price"] = round(stocks[sym]["price"] * (1 + change_pct / 100), 2)
            stocks[sym]["change"] = round(change_pct, 2)

        # Fluctuate forex
        for pair in forex:
            forex[pair] = round(forex[pair] * (1 + random.uniform(-0.05, 0.05) / 100), 4)

        # Push to all clients
        socketio.emit('live_update', {
            "stocks": stocks,
            "forex":  forex,
            "time":   datetime.now().strftime("%H:%M:%S")
        })

# ── SOCKET EVENTS ──────────────────────────────────────
@socketio.on('connect')
def on_connect():
    emit('init_data', {
        "account":  account,
        "stocks":   stocks,
        "forex":    forex,
        "time":     datetime.now().strftime("%H:%M:%S")
    })

@socketio.on('user_message')
def handle_message(data):
    user_input = data.get('message', '').strip().lower()
    time.sleep(0.3)

    # Smart intent routing
    if any(w in user_input for w in ['balance', 'money', 'funds', 'account']):
        response = (f"💰 Your current account balance is ₹{account['balance']:,.2f} "
                    f"and savings balance is ₹{account['savings']:,.2f}.")
    elif any(w in user_input for w in ['transaction', 'history', 'recent', 'spent']):
        txns = account['transactions'][:3]
        lines = "\n".join([f"• {t['date']}: {t['desc']} ({'+'if t['amount']>0 else ''}₹{abs(t['amount']):,})" for t in txns])
        response = f"📋 Recent transactions:\n{lines}"
    elif any(w in user_input for w in ['stock', 'market', 'share', 'equity', 'nifty']):
        lines = "\n".join([f"• {s}: ₹{stocks[s]['price']:,.2f} ({'+' if stocks[s]['change']>0 else ''}{stocks[s]['change']}%)" for s in stocks])
        response = f"📈 Live Stock Prices:\n{lines}"
    elif any(w in user_input for w in ['forex', 'currency', 'exchange', 'dollar', 'usd', 'euro', 'rate']):
        lines = "\n".join([f"• {p}: ₹{forex[p]}" for p in forex])
        response = f"💱 Live Exchange Rates:\n{lines}"
    elif any(w in user_input for w in ['transfer', 'send', 'pay']):
        response = "💸 To transfer money, go to Payments → New Transfer. Enter UPI ID or account number."
    elif any(w in user_input for w in ['loan', 'borrow', 'emi']):
        response = "🏦 We offer Personal (10%), Home (8.5%), and Car loans (9%). Apply in the Loans section."
    elif any(w in user_input for w in ['card', 'credit', 'debit']):
        response = "💳 Manage your cards under Cards section. Limit: ₹1,00,000. CVV resets every 24h."
    elif any(w in user_input for w in ['help', 'support', 'assist']):
        response = "🙋 Our support team is available 24/7 at 1800-123-456 or support@nexabank.in"
    else:
        response = get_response(user_input)

    emit('bot_response', {'response': response})

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    t = threading.Thread(target=simulate_live_data, daemon=True)
    t.start()
    socketio.run(app, debug=True)

