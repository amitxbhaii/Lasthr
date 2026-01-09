import os
import urllib.parse
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]

app = ApplicationBuilder().token(BOT_TOKEN).build()

# MAIN HANDLER (ultra-light)
async def reply_with_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    q = update.message.text.strip()
    if not q:
        return

    encoded = urllib.parse.quote_plus(q)

    link = (
        "https://www.youtube.com/results"
        f"?search_query={encoded}&sp=EgIIAw%253D%253D"
    )

    await update.message.reply_text(link)

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, reply_with_link)
)

# Vercel entry
async def handler(request):
    data = await request.json()
    update = Update.de_json(data, app.bot)
    await app.process_update(update)
    return {
        "statusCode": 200,
        "body": "ok"
    }
