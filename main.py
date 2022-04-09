import os
import urllib.parse

import requests
from dotenv import load_dotenv

load_dotenv()

BITLINKS_TOKEN = os.getenv("TOKEN")


def shorten_link(token: str, url: str) -> str:
    """From long ling to short link"""
    url_bitlinks = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        "long_url": url
    }
    response = requests.post(url_bitlinks, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['id']


def parse_link(url: str) -> str:
    """Return netloc + path from url"""
    parsed = urllib.parse.urlparse(url)
    return parsed.netloc + parsed.path


def count_clicks(token: str, bitlink: str, unit: str = 'day', units: int = -1) -> int:
    """Count clicks on bitlink"""
    url_clicks_summary = f'https://api-ssl.bitly.com/v4/bitlinks/{parse_link(bitlink)}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    payload = {
        "unit": unit,
        "units": units,
    }
    response = requests.get(url_clicks_summary, headers=headers, params=payload)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(bitlink):
    """Check url for bitlink"""
    check_bitlink_url = f'https://api-ssl.bitly.com/v4/bitlinks/{parse_link(bitlink)}'
    headers = {
        'Authorization': f'Bearer {BITLINKS_TOKEN}',
    }
    response = requests.get(check_bitlink_url, headers=headers)
    return response.ok


def main():
    """Start program"""
    link = input('Введите ссылку: ')
    try:
        response = requests.get(link)
        response.raise_for_status()
        if is_bitlink(link):
            clicks_count = count_clicks(BITLINKS_TOKEN, link)
            print('Количество кликов:', clicks_count)
        else:
            bitlink_result = shorten_link(BITLINKS_TOKEN, link)
            print('Битлинк', bitlink_result)
    except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema, requests.exceptions.HTTPError):
        print('Incorrect url')


if __name__ == '__main__':
    main()
