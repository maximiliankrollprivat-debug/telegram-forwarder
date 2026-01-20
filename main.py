import os
import asyncio
from telethon import TelegramClient, events
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Credentials aus Environment Variables
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
PHONE = os.environ.get('PHONE_NUMBER')

# Kanäle die überwacht werden
SOURCE_CHANNELS = [
    'United24media',
    'DIUkraine',
    'OSINTdefender',
    'DeepStateUA',
    'KyivIndependent_official'
]

# Bot Client für Weiterleitung
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# User Client für Kanal-Überwachung
client = TelegramClient('user_session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    try:
        # Nachricht an den Bot weiterleiten
        source = event.chat.username or event.chat.title or "Unknown"
        text = event.message.text or event.message.message or ""
        
        if text:
            formatted = f"📍 **{source}**\n\n{text[:3000]}"
            
            # An alle Bot-Nutzer senden (du musst /start im Bot drücken)
            async for dialog in bot.iter_dialogs():
                if dialog.is_user:
                    try:
                        await bot.send_message(dialog.id, formatted)
                    except Exception as e:
                        logger.error(f"Send error: {e}")
                        
            logger.info(f"Forwarded from {source}")
    except Exception as e:
        logger.error(f"Handler error: {e}")

async def main():
    # User Client starten (braucht einmalige Authentifizierung)
    await client.start(phone=PHONE)
    logger.info("Userbot gestartet!")
    logger.info(f"Überwache: {', '.join(SOURCE_CHANNELS)}")
    
    # Bot starten
    await bot.start(bot_token=BOT_TOKEN)
    logger.info("Bot gestartet!")
    
    # Laufen lassen
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
```

4. Klicke unten auf **"Commit changes"** → **"Commit changes"**

---

### Datei 2: `requirements.txt`

1. Klicke auf **"Add file"** → **"Create new file"**
2. Name: `requirements.txt`
3. Füge ein:
```
telethon==1.34.0
python-dotenv==1.0.0
