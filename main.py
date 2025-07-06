import re
from telegram import Update, ChatMember, MessageEntity
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

import os
BOT_TOKEN = os.environ.get("BOT_TOKEN")

patterns = [
    r"https?://\S+",
    r"t\.me/\S+",
    r"@[\w\d_]+"
]

async def delete_blocked_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    message = update.message

    if not message:
        return

    member = await chat.get_member(user.id)
    if member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        return

    # Check plain text
    text = message.text or message.caption or ""
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            await message.delete()
            return

    # Check for hidden hyperlinks
    if message.entities:
        for entity in message.entities:
            if entity.type in [MessageEntity.URL, MessageEntity.TEXT_LINK]:
                await message.delete()
                return

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT | filters.Caption, delete_blocked_messages))
print("Bot is running...")

# Flask mini-server to keep Replit alive
import threading
from flask import Flask, request

app_keep_alive = Flask('')

@app_keep_alive.route('/')
def home():
    return "Bot is running!"

def run_web():
    app_keep_alive.run(host='0.0.0.0', port=8080)

# Start the Flask server and the Telegram bot
threading.Thread(target=run_web).start()
app.run_polling()
