
import requests
import time
import json

# Load the scan_clause payload from JSON file
with open("chartink_bull_prime_p1_payload.json") as f:
    payload = json.load(f)

# Replace this with your actual Make.com webhook URL
webhook_url = "https://hook.us2.make.com/1o55lghyu7zhsp8bbxejcysqbrwz77xc"

seen = set()

def get_results():
    try:
        response = requests.post("https://chartink.com/screener/process", data=payload)
        return response.json().get("data", [])
    except Exception as e:
        print("Error fetching Chartink data:", e)
        return []

while True:
    try:
        results = get_results()
        for stock in results:
            symbol = stock.get('nsecode')
            if symbol and symbol not in seen:
                seen.add(symbol)
                print(f"New stock found: {symbol}")
                # Send to Make.com webhook
                requests.post(webhook_url, json=stock)
        time.sleep(60)  # Run every 60 seconds
    except Exception as e:
        print("Unexpected error:", e)
        time.sleep(60)
