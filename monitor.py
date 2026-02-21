import requests
import json
import os

LINE_TOKEN = "LINE TOKEN"

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
    requests.post("https://api.line.me/v2/bot/message/push",
                  headers=headers,
                  data=json.dumps(data))

def check_products():
    r = requests.get(PRODUCTS_URL)
    products = r.json()["products"]

    found = []

    for p in products:
        title = p["title"]
        for variant in p["variants"]:
            if variant["available"]:
                found.append(title)

    if found:
        message = "🔥 ハズビン再販検知！\n\n" + "\n".join(found)
        send_line(message)

if __name__ == "__main__":
    check_products()
