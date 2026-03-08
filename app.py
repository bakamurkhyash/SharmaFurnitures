from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.api
from cloudinary.utils import cloudinary_url
import requests
import asyncio
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, ContextTypes

CLOUDINARY_CLOUD_NAME = "dlkjvnxpu"
CLOUDINARY_API_KEY = "288393286726996"
CLOUDINARY_API_SECRET = "i3pm1Q9GRnMwY-HAh62mbj1caz0"

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8088454102:AAEbeQN_szEn2nGs9pKLCAzyZegoWphU7CY"
TELEGRAM_CHAT_ID = "7462545196"
VERCEL_URL = "https://sharma-furnitures-seven.vercel.app/"  # Replace with your actual Vercel URL

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

result = cloudinary.api.resources(type="upload", max_results=500)


@app.route('/')
def index():
    return render_template('index.html', images=result.get('resources', [])[:6])


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    async def process():
        from bot import get_bot_app
        bot_app = get_bot_app()
        await bot_app.initialize()
        await bot_app.process_update(Update.de_json(data, bot_app.bot))
        await bot_app.shutdown()

    asyncio.run(process())
    return jsonify({"ok": True})


@app.route("/set-webhook", methods=["GET"])
def set_webhook():
    async def register():
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.set_webhook(f"{VERCEL_URL}/webhook")

    asyncio.run(register())
    return jsonify({"ok": True, "webhook": f"{VERCEL_URL}/webhook"})


@app.route('/gallery')
def gallery():
    return result


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', images=result.get('resources', []))


@app.route('/calculator')
def calculator():
    return render_template('calculator.html')


if __name__ == '__main__':
    app.run(debug=True)