
import os
import logging

LOG_FILE_PATH = os.getenv("LOG_FILE_PATH")

TELEBOT_DEBUG_ENABLED = False

TELEBOT_DEBUG_LEVEL = None
if TELEBOT_DEBUG_ENABLED:
    TELEBOT_DEBUG_LEVEL = logging.DEBUG


logging.basicConfig(filename=LOG_FILE_PATH, level=TELEBOT_DEBUG_LEVEL,
                    format='%(asctime)s %(message)s')


logger = logging.getLogger('telegram-loyalty')
logger.setLevel(logging.DEBUG)

_api = None

def api():
    return _api
