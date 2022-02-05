from datetime import datetime
import os
from pprint import pprint
from urllib.parse import urlparse

import requests


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
        response = requests.get(url)
        response.raise_for_status()
        with open(f'{file_path}{file_name}', 'wb') as file:
            file.write(response.content)


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
        response = requests.get(url)
        response.raise_for_status()
        with open(f'{file_path}{file_name}', 'wb') as file:
            file.write(response.content)


def fetch_image_epic():
    file_path = 'images/EPIC/'
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    epic_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {
        'api_key': 'sFB6SYeX9LtE6EYuY9yj7eq8ikb0QBE8IahIJOaS'
    }
    response = requests.get(epic_url, params=params)
    response.raise_for_status()
    for image_number, image_url in enumerate(response.json()):
        file_name = f'epic_{image_number}.png'
        # date = image_url['date'][:10].replace('-', '/')
        # date = datetime.fromisoformat(image_url['date'])
        date = datetime.strptime(image_url['date'])
        print(date)
        image = image_url['image']
        epic_url2 = f'https://api.nasa.gov/EPIC/archive/natural/{date.year}/{date.month}/{date.day}/png/{image}.png'
        print(epic_url2)
        response = requests.get(epic_url2, params=params)
        response.raise_for_status()
        with open(f'{file_path}{file_name}', 'wb') as file:
            file.write(response.content)


def main():
    flight_number = 110
    fetch_image_spacex_launch(flight_number)
    # fetch_image_nasa(7)
    fetch_image_epic()


if __name__ == "__main__":
    main()


#  https://api.nasa.gov/planetary/apod?api_key=sFB6SYeX9LtE6EYuY9yj7eq8ikb0QBE8IahIJOaS
