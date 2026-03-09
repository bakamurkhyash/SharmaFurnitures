from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.api
from cloudinary.utils import cloudinary_url
import requests
import asyncio
from telegram import Update, Bot
from bot import *
import threading

CLOUDINARY_CLOUD_NAME = "dlkjvnxpu"
CLOUDINARY_API_KEY = "288393286726996"
CLOUDINARY_API_SECRET = "i3pm1Q9GRnMwY-HAh62mbj1caz0"

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8088454102:AAEbeQN_szEn2nGs9pKLCAzyZegoWphU7CY"
TELEGRAM_CHAT_ID = "7462545196"
WEBHOOK_URL = "https://sharmafurnitures.onrender.com/webhook"

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

# Initialize bot application
bot_app = setup_bot()

@app.route('/')
def index():
    result = cloudinary.api.resources(type="upload", max_results=6)
    return render_template('index.html', images=result.get('resources', []))

@app.route('/gallery')
def gallery():
    result = cloudinary.api.resources(type="upload", max_results=500)
    return result

@app.route('/portfolio')
def portfolio():
    result = cloudinary.api.resources(type="upload", max_results=500)
    return render_template('portfolio.html', images=result.get('resources', []))

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

@app.route('/webhook', methods=['POST'])
async def webhook():
    """Handle incoming Telegram updates via Webhook."""
    try:
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        await bot_app.process_update(update)
        return 'OK', 200
    except Exception as e:
        print(f"Webhook error: {e}")
        return 'Error', 500

@app.route('/set_webhook')
async def set_webhook():
    """Manually trigger webhook registration with Telegram."""
    success = await bot_app.bot.set_webhook(WEBHOOK_URL)
    return f"Webhook set to {WEBHOOK_URL}: {success}"

def start_bot_async():
    """Initialize bot application in the background."""
    asyncio.run(bot_app.initialize())

if __name__ == '__main__':
    # Initialize bot in background
    threading.Thread(target=start_bot_async, daemon=True).start()
    
    # Run Flask
    app.run(debug=True, use_reloader=False)
else:
    # Production (e.g. Gunicorn)
    # Start bot initialization in a separate thread to avoid blocking worker startup
    threading.Thread(target=start_bot_async, daemon=True).start()