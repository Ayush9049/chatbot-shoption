from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()

VERIFY_TOKEN = "farmer_bot_123"


@app.get("/webhook")
def verify_webhook(request: Request):

    # Read query params exactly as Meta sends them
    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    print("MODE:", mode)
    print("TOKEN:", token)
    print("CHALLENGE:", challenge)

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse("verification_failed")

# =========================
# INCOMING WHATSAPP MESSAGES
# =========================
from fastapi.responses import PlainTextResponse

@app.post("/webhook")
async def webhook(request: Request):

    try:
        data = await request.json()
        print("Incoming WhatsApp payload:")
        print(data)

    except Exception as e:
        print("Empty or invalid JSON received:", e)
        return PlainTextResponse("ok")

    return PlainTextResponse("ok")