import os

from dotenv import load_dotenv


load_dotenv()

# BOT_TOKEN = "7249176599:AAHBDwZ_xK0qXNE04tLZAQxePlNd8NxYSMY"
BOT_TOKEN = os.getenv("BOT_TOKEN")
# BOT_TOKEN = "7531971560:AAEx67VUiUNyANcGCIMydZ8HkXKQmyYAfXI"
CHAT_ID = '-1002154658638'

DEFAULT_COMMANDS = (
    ("start", "Start bot"),
    ("book", "book"),
    ("help", ""),
)
