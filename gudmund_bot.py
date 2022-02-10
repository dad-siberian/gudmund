import os
import time

from dotenv import load_dotenv
from telegram.ext import Updater


def posting_photos_telegram_channel(telegram_api, chat_id, timeout):
    updater = Updater(token=telegram_api, use_context=True)
    dispatcher = updater.dispatcher
    for root, dirs, files in os.walk("images"):
        for filename in files:
            photo = os.path.join(root, filename)
            with open(photo, 'rb') as file:
                dispatcher.bot.send_photo(
                    chat_id=chat_id,
                    photo=file
                )
            time.sleep(int(timeout))


def main():
    load_dotenv()
    telegram_api = os.getenv('TELEGRAM_API')
    timeout = os.getenv('TIMEOUT')
    chat_id = os.getenv('CHAT_ID')
    posting_photos_telegram_channel(telegram_api, chat_id, timeout)


if __name__ == '__main__':
    main()
