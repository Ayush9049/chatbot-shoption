from fastapi import FastAPI, Request
import uvicorn
import os

app = FastAPI(title="Minimal FastAPI Server")

# IMPORTANT: keep ONE source of truth
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "farmer_bot_2026")


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


# =========================
# META WEBHOOK VERIFICATION
# =========================
@app.get("/webhook")
def verify_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):

    # Meta sends verification request
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)

    return "verification_failed"


# =========================
# INCOMING WHATSAPP MESSAGES
# =========================
@app.post("/webhook")
async def webhook(request: Request):

    data = await request.json()

    print("Incoming WhatsApp payload:")
    print(data)

    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )