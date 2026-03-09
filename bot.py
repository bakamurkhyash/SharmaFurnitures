from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import asyncio
import os
import tempfile
import cloudinary.uploader

CLOUDINARY_CLOUD_NAME = "dlkjvnxpu"
CLOUDINARY_API_KEY = "288393286726996"
CLOUDINARY_API_SECRET = "i3pm1Q9GRnMwY-HAh62mbj1caz0"

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

# Buffer to collect media group images
media_groups: dict[str, list] = {}
image_names = []
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    photo = message.photo[-1]
    
    print(f"RECEIVED REQUEST: Image detected. Group ID: {message.media_group_id}")

    if message.media_group_id:
        group_id = message.media_group_id
        
        # Add to buffer
        if group_id not in media_groups:
            media_groups[group_id] = []
            # Schedule processing after short delay (to collect all in group)
            context.job_queue.run_once(
                process_media_group,
                when=1.5,  # wait 1.5s for all messages to arrive
                data=group_id,
                name=group_id
            )
        
        media_groups[group_id].append(photo)
    else:
        # Single image
        await download_photo(photo, context)

async def process_media_group(context: ContextTypes.DEFAULT_TYPE):
    group_id = context.job.data
    photos = media_groups.pop(group_id, [])
    
    print(f"Downloading {len(photos)} images from group {group_id}")
    for i, photo in enumerate(photos):
        await download_photo(photo, context, filename=f"{group_id}_{i}.jpg")

async def download_photo(photo, context, filename=None):
    file = await context.bot.get_file(photo.file_id)
    name = filename or f"{photo.file_id}.jpg"
    
    # Use /tmp directory which is writable on Vercel/Render
    temp_dir = tempfile.gettempdir()
    filepath = os.path.join(temp_dir, name)
    
    image_names.append(name)
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

def setup_bot():
    token = "8088454102:AAEbeQN_szEn2nGs9pKLCAzyZegoWphU7CY"
    app = Application.builder().token(token).build()
    ALLOWED_CHAT_ID = 7462545196

    app.add_handler(MessageHandler(
        filters.PHOTO & filters.Chat(ALLOWED_CHAT_ID),
        handle_image
    ))
    return app

def main():
    app = setup_bot()
    app.run_polling()

if __name__ == "__main__":
    main()
