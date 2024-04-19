import os
import logging
import zipfile
import os
from logging.handlers import TimedRotatingFileHandler

# BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_TOKEN = "7066888930:AAHrp16h-XlnYpVfS244TSn_x5dcgDk0Iog"



DEFAULT_COMMANDS = (
    ('start', "Start bot"),
    ('help', "Show help"),
)


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename):
        super().__init__(filename, when='H', interval=2, backupCount=0)
        self.suffix = "%Y-%m-%d_%H-%M-%S"

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = self.rotation_filename("%s.%d.zip" % (self.baseFilename, i))
                dfn = self.rotation_filename("%s.%d.zip" % (self.baseFilename, i + 1))
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.rotation_filename(self.baseFilename + ".1.zip")
            if os.path.exists(dfn):
                os.remove(dfn)
            with zipfile.ZipFile(dfn, 'w') as zf:
                zf.write(self.baseFilename, os.path.basename(self.baseFilename))
            os.remove(self.baseFilename)
        if not self.delay:
            self.stream = self._open()


logger = logging.getLogger()
handler = CustomTimedRotatingFileHandler("logs.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
