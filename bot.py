from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import asyncio
import os

# Buffer to collect media group images
media_groups: dict[str, list] = {}
image_names = []
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    photo = message.photo[-1]

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
    image_names.append(name)
    await file.download_to_drive(str(name))
    print(f"Saved: {name}")

def main():
    app = Application.builder().token("8088454102:AAEbeQN_szEn2nGs9pKLCAzyZegoWphU7CY").build()
    ALLOWED_CHAT_ID = 7462545196

    app.add_handler(MessageHandler(
        filters.PHOTO & filters.Chat(ALLOWED_CHAT_ID),  # ← built-in filter
        handle_image
    ))
    app.run_polling()
    for i in image_names:
        os.remove(i)
