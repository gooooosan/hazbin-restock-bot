import requests
import json
import os

LINE_TOKEN = os.getenv("LINE_TOKEN")
USER_ID = os.getenv("USER_ID")

BASE_URL = "https://hazbinhotel.com"
PRODUCTS_URL = f"{BASE_URL}/products.json"
STATE_FILE = "stock_state.json"

def send_line(message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_TOKEN}"
    }
    data = {
        "to": USER_ID,
        "messages":[
            {"type":"text","text":message}
        ]
    }
    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        data=json.dumps(data)
    )

def load_previous_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def check_products():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(PRODUCTS_URL, headers=headers)
    data = r.json()

    products = data.get("products", [])
    previous_state = load_previous_state()
    current_state = {}

    restocked = []
    new_products = []

    for p in products:
        title = p["title"]
        handle = p["handle"]
        url = f"{BASE_URL}/products/{handle}"

        available = any(v["available"] for v in p["variants"])

        current_state[title] = available

        product_text = f"{title}\n{url}"

        if title not in previous_state:
            new_products.append(product_text)

        elif previous_state[title] is False and available is True:
            restocked.append(product_text)

    messages = []

    if new_products:
        messages.append("🆕 新商品追加！\n\n" + "\n\n".join(new_products))

    if restocked:
        messages.append("🔥 再販検知！\n\n" + "\n\n".join(restocked))

    if messages:
        send_line("\n\n".join(messages))

    save_state(current_state)

if __name__ == "__main__":
    check_products()
