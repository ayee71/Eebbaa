   
import asyncio
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = int(os.environ.get("TELEGRAM_API_ID", "36191585"))
API_HASH = os.environ.get("TELEGRAM_API_HASH", "c4a7610272411c513373141b2c9431e1")
PHONE = os.environ.get("TELEGRAM_PHONE", "+251915030171")
CHANNEL = os.environ.get("TELEGRAM_CHANNEL", "@ayelebeharmee")
OUTPUT_FILE = os.environ.get("OUTPUT_FILE", "telegram_posts.json")
MAX_POSTS = int(os.environ.get("MAX_POSTS", "50"))


def validate_config():
    """Environment variables qulqulluu ta'uu mirkaneessa"""
    if not API_ID or not API_HASH or not PHONE:
        print("✗ Dogoggora: TELEGRAM_API_ID, TELEGRAM_API_HASH, fi TELEGRAM_PHONE guutamuu qabu!")
        sys.exit(1)


def parse_message(message, channel_username):
    """Message Telegram irraa data website-f mijatu baasa"""
    clean_channel = channel_username.replace("@", "")
    text_content = message.text.strip() if message.text else ""
    
    # Gosa media adda baasuu
    media_type = "none"
    if message.photo:
        media_type = "photo"
    elif message.video:
        media_type = "video"
    elif message.document:
        media_type = "document"

    return {
        "id": message.id,
        "source": "Telegram",
        "channel": clean_channel,
        "content": text_content,
        "date": message.date.isoformat() if message.date else "",
        "formatted_date": message.date.strftime("%b %d, %Y - %H:%M") if message.date else "",
        "views": getattr(message, "views", 0) or 0,
        "forwards": getattr(message, "forwards", 0) or 0,
        "link": f"https://t.me/{clean_channel}/{message.id}",
        "has_media": message.media is not None,
        "media_type": media_type
    }


async def fetch_telegram_messages():
    """Telegram channel irraa ergaawwan ariitiidhaan fidaa"""
    validate_config()
    
    # Async Client context manager fayyadamuun connection amansiisaa godha
    async with TelegramClient("telegram_session", int(API_ID), API_HASH) as client:
        await client.start(phone=PHONE)
        print(f"⚡ {CHANNEL} irraa ergaawwan {MAX_POSTS} dhiyeenyaa haaromsaa jira...")

        posts = []
        # Ergaawwan fiduu
        async for message in client.iter_messages(CHANNEL, limit=MAX_POSTS):
            if not message.text and not message.media:
                continue

            parsed_post = parse_message(message, CHANNEL)
            posts.append(parsed_post)

        # Temp file keessatti saavii godhuun dogoggora dubbisa website hir'isa
        temp_file = f"{OUTPUT_FILE}.tmp"
        payload = {
            "last_updated": datetime.now().isoformat(),
            "count": len(posts),
            "posts": posts
        }

        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

        # Temp file gara output file jijjiiruu
        os.replace(temp_file, OUTPUT_FILE)
        print(f"✓ Ergaawwan {len(posts)} milkaa'inaan '{OUTPUT_FILE}' keessatti saavii ta'aniiru!")


if __name__ == "__main__":
    try:
        asyncio.run(fetch_telegram_messages())
    except KeyboardInterrupt:
        print("\nProgramiin dhaabateera.")
    except Exception as e:
        print(f"\n✗ Dogoggora uumameera: {str(e)}")
