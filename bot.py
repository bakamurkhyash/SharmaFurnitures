import asyncio
import os
import tempfile
import cloudinary.uploader
from telegram import Update, Bot

CLOUDINARY_CLOUD_NAME = "dlkjvnxpu"
CLOUDINARY_API_KEY = "288393286726996"
CLOUDINARY_API_SECRET = "i3pm1Q9GRnMwY-HAh62mbj1caz0"

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

async def handle_image(update: Update, bot: Bot):
    """Stateless handler to process individual images."""
    message = update.message
    if not message or not message.photo:
        return
        
    photo = message.photo[-1]
    
    print(f"RECEIVED REQUEST: Image detected. Group ID: {message.media_group_id}")

    # Process immediately and synchronously (no job queues)
    await download_photo(photo, bot, filename=f"{photo.file_id}.jpg")


async def download_photo(photo, bot: Bot, filename=None):
    """Download photo from Telegram and upload securely to Cloudinary."""
    file = await bot.get_file(photo.file_id)
    name = filename or f"{photo.file_id}.jpg"
    
    # Use /tmp directory which is writable on Vercel/Render
    temp_dir = tempfile.gettempdir()
    filepath = os.path.join(temp_dir, name)
    
    try:
        print(f"Downloading to: {filepath}")
        await file.download_to_drive(str(filepath))
        print("Download successful. Starting Cloudinary upload...")
        await asyncio.to_thread(cloudinary.uploader.upload, str(filepath))
        print(f"Uploaded and Saved: {name}")
    except Exception as e:
        print(f"Error uploading {name}: {e}")
    finally:
        if os.path.exists(filepath):
            os.remove(str(filepath))
            print(f"Cleaned up temporary file: {filepath}")
