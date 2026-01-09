import os
import json
import urllib.parse
import requests
from http.server import BaseHTTPRequestHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers.get("content-length", 0))
        body = json.loads(self.rfile.read(length))

        message = body.get("message")
        if not message:
            self.send_response(200)
            self.end_headers()
            return

        chat_id = message["chat"]["id"]
        text = message.get("text")

        if text:
            query = urllib.parse.quote_plus(text.strip())
            yt_link = (
                "https://www.youtube.com/results"
                f"?search_query={query}&sp=EgIIAw%253D%253D"
            )

            requests.post(
                f"{API_URL}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": yt_link
                },
                timeout=3
            )

        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"YT Last Hour Bot Running")
