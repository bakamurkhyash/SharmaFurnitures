from flask import Flask, render_template, request, jsonify
import cloudinary
import cloudinary.api
from cloudinary.utils import cloudinary_url
import requests
import asyncio
from telegram import Update, Bot
from bot import *
from telegram.ext import Application, MessageHandler, filters, ContextTypes

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


if __name__ == '__main__':
    import threading

    threading.Thread(target=main, daemon=True).start()
    
    app.run(debug=True, use_reloader=False)