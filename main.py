from fastapi import FastAPI, Request
import uvicorn
import os

app = FastAPI(title="Minimal FastAPI Server")

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "mytoken")


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


# Meta webhook verification
@app.get("/webhook")
def verify_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):
    if hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)

    return {"error": "verification failed"}


# Incoming WhatsApp messages
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