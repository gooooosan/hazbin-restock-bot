import requests
import json
import os

LINE_TOKEN = os.getenv("LINE_TOKEN")
USER_ID = os.getenv("USER_ID")

PRODUCTS_URL = "https://hazbinhotel.com/products.json"

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

def check_products():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(PRODUCTS_URL, headers=headers, timeout=10)
        r.raise_for_status()

        data = r.json()
        products = data.get("products", [])

        found = []

        for p in products:
            title = p["title"]
            for variant in p["variants"]:
                if variant["available"]:
                    found.append(title)

        if found:
            message = "🔥 ハズビン再販検知！\n\n" + "\n".join(found)
            send_line(message)
        else:
            print("在庫なし")

    except Exception as e:
        print("エラー:", e)

if __name__ == "__main__":
    check_products()
