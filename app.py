import requests
import time
from flask import Flask
import os

app = Flask(__name__)

# Telegram setup (replace with your values)
telegram_token = "7596334291:AAEJX2cy22V8_KDIMxmBxtmyRiqjvTaRD08"
chat_id = "7091936835"

# Function to send Telegram message
def send_telegram(message):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)

# Get initial Bitcoin price from CoinGecko
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
response = requests.get(url)
initial_price = response.json()["bitcoin"]["usd"]
print(f"Starting Price: ${initial_price}")

# Run the bot in a separate function
def run_bot():
    while True:
        response = requests.get(url)
        current_price = response.json()["bitcoin"]["usd"]
        percent_change = ((current_price - initial_price) / initial_price) * 100

        if percent_change >= 2:
            send_telegram(f"SELL! Bitcoin up {percent_change:.2f}% - Price: ${current_price}")
            print(f"SELL signal sent: ${current_price}")
            break
        elif percent_change <= -2:
            send_telegram(f"BUY! Bitcoin down {percent_change:.2f}% - Price: ${current_price}")
            print(f"BUY signal sent: ${current_price}")
            break

        print(f"Current Price: ${current_price}, Change: {percent_change:.2f}%")
        time.sleep(30)

# Heroku requires a web server
@app.route('/')
def home():
    return "AIX Signal Bot is running!"

if __name__ == "__main__":
    run_bot()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))