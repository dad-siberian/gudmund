import os
from datetime import datetime
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv


def extarct_file_extension(url):
    parse = urlparse(url)
    file_extension = os.path.splitext(parse.path)[1]
    return file_extension


def fetch_image_nasa(nasa_api, file_path, count_image=30):
    nasa_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': nasa_api,
        'count': count_image
    }
    response = requests.get(nasa_url, params=params)
    response.raise_for_status()
    images_urls = [image_url['hdurl'] for image_url in response.json()]
    for image_number, url in enumerate(images_urls, start=1):
        file_name = f'nasa_{image_number}{extarct_file_extension(url)}'
        snapshot = requests.get(url)
        snapshot.raise_for_status()
        with open(f'{file_path}{file_name}', 'wb') as file:
            file.write(snapshot.content)


def fetch_image_epic(nasa_api, file_path):
    recent_snapshots_url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {
        'api_key': nasa_api
    }
    response = requests.get(recent_snapshots_url, params=params)
    response.raise_for_status()
    for image_number, image_url in enumerate(response.json(), start=1):
        file_name = f'epic_{image_number}.png'
        shooting_date = datetime.strptime(
            image_url['date'],
            "%Y-%m-%d %H:%M:%S"
            ).strftime("%Y/%m/%d")
        image_name = image_url['image']
        snapshot_url = (
            f'https://api.nasa.gov/EPIC/archive/natural/'
            f'{shooting_date}/png/{image_name}.png'
        )
        snapshot = requests.get(snapshot_url, params=params)
        snapshot.raise_for_status()
        with open(f'{file_path}{file_name}', 'wb') as file:
            file.write(snapshot.content)


def main():
    load_dotenv()
    nasa_api = os.getenv('NASA_API')
    file_paths = {
        'nasa': 'images/NASA/',
        'epic': 'images/EPIC/'
    }
    for path in file_paths.values():
        os.makedirs(path, exist_ok=True)
    fetch_image_nasa(nasa_api, file_paths['nasa'])
    fetch_image_epic(nasa_api, file_paths['epic'])


if __name__ == '__main__':
    main()
