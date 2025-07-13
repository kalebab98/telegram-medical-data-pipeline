import os
import json
import logging
from datetime import datetime, timezone
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, MessageMediaWebPage, MessageMediaContact, MessageMediaGeo, MessageMediaVenue, MessageMediaPoll, MessageMediaDice, MessageMediaGame, MessageMediaInvoice, MessageMediaUnsupported, MessageMediaDocument
from telethon.errors import FloodWaitError
from dotenv import load_dotenv
import argparse
import asyncio
from concurrent.futures import ThreadPoolExecutor
import hashlib
import time
from collections import defaultdict
import shutil

# Load environment variables
load_dotenv()

# Set up logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/scraping.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)

RAW_DATA_DIR = 'data/raw/telegram_messages'
IMAGE_DATA_DIR = 'data/raw/telegram_images'
CHECKPOINT_DIR = 'data/raw/checkpoints'

# Default config
DEFAULT_IMAGE_TYPES = ['image/jpeg', 'image/png']
DEFAULT_KEYWORDS = []  # e.g., ['paracetamol', 'cream', 'pill']

# Helper to hash image content for deduplication
image_hashes = set()

def hash_file(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def load_channels(channel_file):
    with open(channel_file, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

def load_checkpoint(channel_name):
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    checkpoint_file = os.path.join(CHECKPOINT_DIR, f'{channel_name}.json')
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            return json.load(f).get('last_message_id')
    return None

def save_checkpoint(channel_name, last_message_id):
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)
    checkpoint_file = os.path.join(CHECKPOINT_DIR, f'{channel_name}.json')
    with open(checkpoint_file, 'w') as f:
        json.dump({'last_message_id': last_message_id}, f)

async def download_media(message, channel_name, today, client, media_type, image_types):
    media_path = None
    try:
        out_dir = os.path.join(IMAGE_DATA_DIR, today, channel_name)
        os.makedirs(out_dir, exist_ok=True)
        file_name = f"{message.id}"
        if media_type == 'photo':
            file_name += '.jpg'
        elif media_type == 'document':
            ext = '.bin'
            if message.file and message.file.ext:
                ext = message.file.ext
            file_name += ext
        file_path = os.path.join(out_dir, file_name)
        await client.download_media(message, file_path)
        # Deduplication by hash
        file_hash = hash_file(file_path)
        if file_hash in image_hashes:
            os.remove(file_path)
            return None
        image_hashes.add(file_hash)
        # Image type filtering
        if media_type == 'photo' or (media_type == 'document' and message.file and message.file.mime_type in image_types):
            return file_path
        else:
            os.remove(file_path)
            return None
    except Exception as e:
        logging.error(f"Failed to download {media_type} for message {message.id} in {channel_name}: {e}")
    return None

async def scrape_channel(client, channel_url, args, image_types, keywords):
    channel_name = channel_url.split('/')[-1]
    messages_by_date = defaultdict(list)
    images_downloaded = 0
    skipped_messages = 0
    errors = 0
    last_message_id = load_checkpoint(channel_name)
    try:
        iter_kwargs = {
            'entity': channel_url,
            'reverse': True
        }
        if last_message_id is not None:
            iter_kwargs['min_id'] = last_message_id + 1
        if args.start_date:
            iter_kwargs['offset_date'] = args.start_date

        async for message in client.iter_messages(**iter_kwargs):
            # Message filtering by keywords
            if keywords:
                text = (message.text or '').lower()
                if not any(kw.lower() in text for kw in keywords):
                    skipped_messages += 1
                    continue
            msg_dict = {
                'id': message.id,
                'date': str(message.date),
                'sender_id': getattr(message.sender_id, 'user_id', message.sender_id) if hasattr(message, 'sender_id') else None,
                'text': message.text,
                'has_image': False,
                'has_document': False,
                'has_video': False,
                'has_audio': False,
                'media_type': None,
                'local_media_path': None
            }
            # Download images/photos
            if message.photo:
                # Use message date for image folder as well
                msg_date = message.date.strftime('%Y-%m-%d')
                path = await download_media(message, channel_name, msg_date, client, 'photo', image_types)
                if path:
                    msg_dict['has_image'] = True
                    msg_dict['media_type'] = 'photo'
                    msg_dict['local_media_path'] = path
                    images_downloaded += 1
            # Download documents (images, videos, audio)
            elif message.document:
                mime_type = message.file.mime_type if message.file else ''
                if mime_type.startswith('image/') or mime_type.startswith('video/') or mime_type.startswith('audio/'):
                    msg_date = message.date.strftime('%Y-%m-%d')
                    path = await download_media(message, channel_name, msg_date, client, 'document', image_types)
                    if path:
                        if mime_type.startswith('image/'):
                            msg_dict['has_image'] = True
                            msg_dict['media_type'] = 'image_document'
                        elif mime_type.startswith('video/'):
                            msg_dict['has_video'] = True
                            msg_dict['media_type'] = 'video_document'
                        elif mime_type.startswith('audio/'):
                            msg_dict['has_audio'] = True
                            msg_dict['media_type'] = 'audio_document'
                        msg_dict['local_media_path'] = path
                        images_downloaded += 1
            else:
                skipped_messages += 1
            # Group messages by their actual date
            msg_date_obj = message.date
            if args.start_date and msg_date_obj < args.start_date:
                continue
            if args.end_date and msg_date_obj > args.end_date:
                continue
            msg_date = message.date.strftime('%Y-%m-%d')
            messages_by_date[msg_date].append(msg_dict)
            save_checkpoint(channel_name, message.id)
        # Clean old data if --clean is set
        if getattr(args, 'clean', False):
            for msg_date in messages_by_date.keys():
                out_dir = os.path.join(RAW_DATA_DIR, msg_date)
                out_file = os.path.join(out_dir, f'{channel_name}.json')
                if os.path.exists(out_file):
                    os.remove(out_file)
        # Write messages grouped by date
        for msg_date, msgs in messages_by_date.items():
            out_dir = os.path.join(RAW_DATA_DIR, msg_date)
            os.makedirs(out_dir, exist_ok=True)
            out_file = os.path.join(out_dir, f'{channel_name}.json')
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(msgs, f, ensure_ascii=False, indent=2)
        logging.info(f'Successfully scraped messages for {channel_name}. Images downloaded: {images_downloaded}, Skipped: {skipped_messages}, Errors: {errors}')
        print(f"Channel: {channel_name} | Images: {images_downloaded} | Skipped: {skipped_messages} | Errors: {errors}")
    except FloodWaitError as e:
        logging.error(f'FloodWaitError scraping {channel_name}: Must wait {e.seconds} seconds')
        print(f'FloodWaitError: Waiting {e.seconds} seconds for {channel_name}')
        time.sleep(e.seconds)
        return await scrape_channel(client, channel_url, args, image_types, keywords)
    except Exception as e:
        errors += 1
        logging.error(f'Error scraping {channel_name}: {e}')
        print(f'Error scraping {channel_name}: {e}')

async def main():
    parser = argparse.ArgumentParser(description='Telegram Scraper')
    parser.add_argument('--channels', type=str, default='channels.txt', help='Path to channels.txt')
    parser.add_argument('--start-date', type=str, default=None, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, default=None, help='End date (YYYY-MM-DD)')
    parser.add_argument('--keywords', type=str, nargs='*', default=DEFAULT_KEYWORDS, help='Keywords to filter messages')
    parser.add_argument('--image-types', type=str, nargs='*', default=DEFAULT_IMAGE_TYPES, help='Allowed image MIME types')
    parser.add_argument('--parallel', action='store_true', help='Enable parallel scraping')
    parser.add_argument('--clean', action='store_true', help='Delete old data for selected date/channel before rescanning')
    args = parser.parse_args()

    # Parse dates
    if args.start_date:
        args.start_date = datetime.strptime(args.start_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    if args.end_date:
        args.end_date = datetime.strptime(args.end_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)

    # Load channels
    channels = load_channels(args.channels)
    API_ID = os.getenv('TELEGRAM_API_ID')
    API_HASH = os.getenv('TELEGRAM_API_HASH')
    SESSION_NAME = os.getenv('TELEGRAM_SESSION', 'anon')

    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        tasks = []
        for channel in channels:
            if args.parallel:
                tasks.append(scrape_channel(client, channel, args, args.image_types, args.keywords))
            else:
                await scrape_channel(client, channel, args, args.image_types, args.keywords)
        if args.parallel:
            await asyncio.gather(*tasks)
    print('Scraping complete.')

if __name__ == '__main__':
    asyncio.run(main()) 