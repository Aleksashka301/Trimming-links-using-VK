import requests
import os
from dotenv import load_dotenv, find_dotenv
import argparse


def is_shorten_link(token, url):
    params = {
        'access_token': token,
        'url': url,
        'private': '0',
        'v': 5.199,
    }

    response = requests.get('https://api.vk.ru/method/utils.getShortLink', params=params)
    response.raise_for_status()
    return 'error' in response.json().keys()


def shorten_link(token, url):
    params = {
        'access_token': token,
        'url': url,
        'private': '0',
        'v': 5.199,
    }

    response = requests.get('https://api.vk.ru/method/utils.getShortLink', params=params)
    response.raise_for_status()
    return response.json()['response']['short_url']


def count_clicks(token, link):
    params = {
        'access_token': token,
        'key': link[-6:],
        'v': 5.199,
    }

    response = requests.get('https://api.vk.ru/method/utils.getLinkStats', params=params)
    response.raise_for_status()
    return response.json()['response']['stats'][0]['views']


def main():
    load_dotenv(find_dotenv())
    token = os.environ['VK_ACCESS_TOKEN']

    parser = argparse.ArgumentParser()
    parser.add_argument('link')
    args = parser.parse_args()
    user_url = args.link

    if is_shorten_link(token, user_url):
        try:
            print('Количество кликов: ', count_clicks(token, user_url))
        except IndexError:
            print('Переходов по данной ссылке ещё не было!')
    else:
        print('Сокращенная ссылка: ', shorten_link(token, user_url))


if __name__ == '__main__':
    main()