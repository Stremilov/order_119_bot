import os
import logging
import zipfile
import os
from logging.handlers import TimedRotatingFileHandler

BOT_TOKEN = os.getenv('BOT_TOKEN')
# BOT_TOKEN = "7066888930:AAHrp16h-XlnYpVfS244TSn_x5dcgDk0Iog"

DEFAULT_COMMANDS = (
    ('start', "Start bot"),
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
