from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import requests
import os

app = FastAPI()

VERIFY_TOKEN = "farmer_bot_123"

ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


# =========================
# WEBHOOK VERIFY
# =========================
@app.get("/webhook")
def verify_webhook(request: Request):

    params = dict(request.query_params)

    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return PlainTextResponse(params.get("hub.challenge"))

    return PlainTextResponse("verification_failed")


# =========================
# SEND MESSAGE FUNCTION
# =========================
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
        "text": {"body": message}
    }

    response = requests.post(url, headers=headers, json=payload)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)


# =========================
# INCOMING MESSAGES
# =========================
@app.post("/webhook")
async def webhook(request: Request):

    try:
        data = await request.json()
        print("INCOMING:", data)

        value = data["entry"][0]["changes"][0]["value"]

        if "messages" not in value:
            return PlainTextResponse("ok")

        msg = value["messages"][0]["text"]["body"]
        phone = value["messages"][0]["from"]

        print("PHONE:", phone)
        print("MESSAGE:", msg)

        reply = "Namaste 👋 How can I help you today?"
        send_whatsapp_message(phone, reply)

    except Exception as e:
        print("ERROR:", e)

    return PlainTextResponse("ok")


# =========================
# TEST ENDPOINT
# =========================
@app.get("/test-send")
def test_send():

    send_whatsapp_message("919XXXXXXXXX", "Hello 👋 this is your bot")

    return {"status": "sent"}