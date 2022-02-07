import logging
import os
from datetime import datetime
from urllib.parse import urlparse

import requests
from telegram.ext import Updater


TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']


def fetch_image_spacex_launch(flight_number):
    file_path = f'images/spacex/{flight_number}/'
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    spacex_url = f'https://api.spacexdata.com/v3/launches/{flight_number}'
    response = requests.get(spacex_url)
    response.raise_for_status()
    images_urls = response.json()['links']['flickr_images']
    for image_number, url in enumerate(images_urls, 1):
        file_name = f'spacex_{image_number}.jpg'
        snapshot = requests.get(url)
        snapshot.raise_for_status()
        with open(f'{file_path}{file_name}', 'wb') as file:
            file.write(snapshot.content)


def get_file_extension(url):
    parse = urlparse(url)
    file_extension = os.path.splitext(parse.path)[1]
    return file_extension


def fetch_image_nasa(count_image):
    file_path = 'images/NASA/'
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': 'sFB6SYeX9LtE6EYuY9yj7eq8ikb0QBE8IahIJOaS',
        'count': count_image
    }
    response = requests.get(nasa_url, params=params)
    response.raise_for_status()
    images_urls = [image_url['hdurl'] for image_url in response.json()]
    for image_number, url in enumerate(images_urls, 1):
        file_name = f'nasa_{image_number}{get_file_extension(url)}'
        snapshot = requests.get(url)
        snapshot.raise_for_status()
        with open(f'{file_path}{file_name}', 'wb') as file:
            file.write(snapshot.content)


def fetch_image_epic():
    file_path = 'images/EPIC/'
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    recent_snapshots_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {
        'api_key': 'sFB6SYeX9LtE6EYuY9yj7eq8ikb0QBE8IahIJOaS'
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
    # flight_number = 110
    # fetch_image_spacex_launch(flight_number)
    # fetch_image_nasa(1)
    # fetch_image_epic()

    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
    dispatcher.bot.send_photo(chat_id='@gudmund198', photo=open('images/NASA/nasa_6.jpg', 'rb'))
    updater.start_polling()


if __name__ == "__main__":
    main()
