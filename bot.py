from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes, JobQueue
import asyncio
import os
import cloudinary
import glob

app_flask = Flask(__name__)

TOKEN = "YOUR_BOT_TOKEN"
WEBHOOK_URL = "https://yourdomain.com/webhook"  # must be HTTPS
ALLOWED_CHAT_ID = 123456789
img_names = []

# Build the telegram app once
ptb_app = (
    Application.builder()
    .token(TOKEN)
    .job_queue(JobQueue())
    .build()
)

media_groups: dict[str, list] = {}

# ── handlers ────────────────────────────────────────────────

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    photo = message.photo[-1]

    if message.media_group_id:
        group_id = message.media_group_id
        if group_id not in media_groups:
            media_groups[group_id] = []
            context.job_queue.run_once(process_media_group, when=1.5, data=group_id, name=group_id)
        media_groups[group_id].append(photo)
    else:
        await download_photo(photo, context)

async def process_media_group(context: ContextTypes.DEFAULT_TYPE):
    group_id = context.job.data
    photos = media_groups.pop(group_id, [])
    for i, photo in enumerate(photos):
        await download_photo(photo, context, filename=f"{group_id}_{i}.jpg")

async def download_photo(photo, context, filename=None):
    file = await context.bot.get_file(photo.file_id)
    name = filename or f"{photo.file_id}.jpg"
    os.makedirs("images", exist_ok=True)
    await file.download_to_drive(f"images/{name}")
    img_names.append(f"images/{name}")
    print(f"Saved: {name}")

async def upload_images():
    for img in img_names:
        cloudinary.uploader.upload(img)
