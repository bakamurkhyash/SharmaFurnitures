import os
import asyncio
import cloudinary
import cloudinary.uploader
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from app import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET


cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
)

ALLOWED_CHAT_ID = 7462545196  # Replace with your specific chat ID

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ignore everyone except the specific person
    if update.effective_chat.id != ALLOWED_CHAT_ID:
        return

    try:
        file = await context.bot.get_file(update.message.photo[-1].file_id)
        cloudinary.uploader.upload(file.file_path, folder="telegram-uploads", resource_type="image")
    except Exception as e:
        print(f"Upload error: {e}")


def get_bot_app() -> Application:
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).updater(None).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    return app
