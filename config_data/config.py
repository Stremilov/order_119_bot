import logging
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')

DEFAULT_COMMANDS = (
    ('start', "Start bot"),
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
