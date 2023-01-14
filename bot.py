from os import environ
import logging
from aiogram import Bot, executor

from handlers.handlers import *


TOKEN = environ.get('TG_BOT_GOOGLE_DRIVE')
bot = Bot(token=TOKEN)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
