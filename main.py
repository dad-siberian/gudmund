import os
import time
from datetime import datetime
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from telegram.ext import Updater


def fetch_image_spacex_launch():
    file_path = 'images/spacex/'
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    spacex_url = 'https://api.spacexdata.com/v3/launches/97'
    response = requests.get(spacex_url)
    response.raise_for_status()
    images_urls = response.json()['links']['flickr_images']
    for image_number, url in enumerate(images_urls):
        file_name = f'spacex_{image_number}.jpg'
        snapshot = requests.get(url)
        snapshot.raise_for_status()
        with open(f'{file_path}{file_name}', 'wb') as file:
            file.write(snapshot.content)


def get_file_extension(url):
    parse = urlparse(url)
    file_extension = os.path.splitext(parse.path)[1]
    return file_extension


def fetch_image_nasa(nasa_api, count_image):
    file_path = 'images/NASA/'
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': nasa_api,
        'count': count_image
    }
    response = requests.get(nasa_url, params=params)
    response.raise_for_status()
    images_urls = [image_url['hdurl'] for image_url in response.json()]
    for image_number, url in enumerate(images_urls):
        file_name = f'nasa_{image_number}{get_file_extension(url)}'
        snapshot = requests.get(url)
        snapshot.raise_for_status()
        with open(f'{file_path}{file_name}', 'wb') as file:
            file.write(snapshot.content)


def fetch_image_epic(nasa_api):
    file_path = 'images/EPIC/'
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    recent_snapshots_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {
        'api_key': nasa_api
    }
    response = requests.get(recent_snapshots_url, params=params)
    response.raise_for_status()
    for image_number, image_url in enumerate(response.json()):
        file_name = f'epic_{image_number}.png'
        shooting_date = datetime.strptime(
            image_url['date'],
            "%Y-%m-%d %H:%M:%S"
            ).strftime("%Y/%m/%d")
        image = image_url['image']
        snapshot_url = (
            f'https://api.nasa.gov/EPIC/archive/natural/'
            f'{shooting_date}/png/{image}.png'
        )
        snapshot = requests.get(snapshot_url, params=params)
        snapshot.raise_for_status()
        with open(f'{file_path}{file_name}', 'wb') as file:
            file.write(snapshot.content)


def main():
    load_dotenv()
    nasa_api = os.getenv('NASA_API')
    telegram_api = os.getenv('TELEGRAM_API')
    timeout = os.getenv('TIMEOUT')
    chat_id = os.getenv('CHAT_ID')
    fetch_image_spacex_launch()
    fetch_image_nasa(nasa_api, 3)
    fetch_image_epic(nasa_api)
    updater = Updater(token=telegram_api, use_context=True)
    dispatcher = updater.dispatcher
    for root, dirs, files in os.walk("images"):
        for filename in files:
            photo = os.path.join(root, filename)
            dispatcher.bot.send_photo(
                chat_id=chat_id,
                photo=open(photo, 'rb')
            )
            time.sleep(int(timeout))
    updater.start_polling()


if __name__ == '__main__':
    main()
