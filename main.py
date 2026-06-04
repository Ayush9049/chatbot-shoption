from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

VERIFY_TOKEN = "farmer_bot_123"


@app.get("/webhook")
def verify_webhook(request: Request):

    params = dict(request.query_params)

    VERIFY_TOKEN = "farmer_bot_123"

    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return PlainTextResponse(params.get("hub.challenge"))

    return PlainTextResponse("verification_failed")

# =========================
# INCOMING WHATSAPP MESSAGES
# =========================
from fastapi.responses import PlainTextResponse

@app.post("/webhook")
async def webhook(request: Request):

    try:
        data = await request.json()
        print("INCOMING:", data)

        # extract message
        msg = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]

        # extract phone number
        phone = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]

        print("PHONE:", phone)
        print("MESSAGE:", msg)

        # AUTO REPLY
        send_whatsapp_message(phone, "Namaste 👋 How can I help you today?")

    except Exception as e:
        print("ERROR:", e)

    return PlainTextResponse("ok")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

import requests
import os

ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


def send_whatsapp_message(to, message):

    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    print("WhatsApp response:", response.status_code, response.text)