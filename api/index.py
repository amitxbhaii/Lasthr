import os
import json
import urllib.parse
import requests
from fastapi import FastAPI, Request

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = FastAPI()

def send_message(chat_id, text):
    requests.post(
        f"{API_URL}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=3
    )

@app.post("/")
async def webhook(req: Request):
    body = await req.json()

    message = body.get("message")
    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    text = message.get("text")

    if not text:
        return {"ok": True}

    query = urllib.parse.quote_plus(text.strip())

    yt_link = (
        "https://www.youtube.com/results"
        f"?search_query={query}&sp=EgIIAw%253D%253D"
    )

    send_message(chat_id, yt_link)
    return {"ok": True}

@app.get("/")
def root():
    return {"status": "YT Last Hour Bot Running"}
