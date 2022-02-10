import os

import requests


def fetch_image_spacex_launch(file_path, flight_number='latest'):
    spacex_url = f'https://api.spacexdata.com/v3/launches/{flight_number}'
    response = requests.get(spacex_url)
    response.raise_for_status()
    images_urls = response.json()['links']['flickr_images']
    for image_number, url in enumerate(images_urls, start=1):
        file_name = f'spacex_{flight_number}_{image_number}.jpg'
        snapshot = requests.get(url)
        snapshot.raise_for_status()
        with open(f'{file_path}{file_name}', 'wb') as file:
            file.write(snapshot.content)


def main():
    file_path = 'images/spacex/'
    os.makedirs(file_path, exist_ok=True)
    fetch_image_spacex_launch(file_path)


if __name__ == '__main__':
    main()
