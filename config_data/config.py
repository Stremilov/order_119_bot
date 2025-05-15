import os

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = '-1002154658638'

DEFAULT_COMMANDS = (
    ("start", "Start bot"),
    ("book", "book"),
    ("help", ""),
)
