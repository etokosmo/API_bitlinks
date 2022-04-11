import os
import urllib.parse

import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, MissingSchema, HTTPError

BITLINK_API_URL = 'https://api-ssl.bitly.com/v4/bitlinks/'


def shorten_link(entered_long_url: str, header: dict) -> str:
    """From long ling to short link"""
    url_bitlinks = f'{BITLINK_API_URL}'
    payload = {
        "long_url": entered_long_url
    }
    response = requests.post(url_bitlinks, headers=header, json=payload)
    response.raise_for_status()
    return response.json()['id']


def parse_link(long_url: str) -> str:
    """Return netloc + path from url"""
    parsed = urllib.parse.urlparse(long_url)
    return parsed.netloc + parsed.path


def count_clicks(entered_bitlink: str, header: dict, unit: str = 'day', units: int = -1) -> int:
    """Count clicks on bitlink"""
    url_clicks_summary = f'{BITLINK_API_URL}{parse_link(entered_bitlink)}/clicks/summary'
    payload = {
        "unit": unit,
        "units": units,
    }
    response = requests.get(url_clicks_summary, headers=header, params=payload)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(entered_link: str, header: dict) -> bool:
    """Check url for bitlink"""
    check_bitlink_url = f'{BITLINK_API_URL}{parse_link(entered_link)}'
    response = requests.get(check_bitlink_url, headers=header)
    return response.ok


def main():
    """Start program"""
    load_dotenv()
    bitlink_token = os.getenv("TOKEN")
    bitlink_header = {'Authorization': f'Bearer {bitlink_token}'}
    entered_link = input('Введите ссылку: ')
    try:
        response = requests.get(entered_link)
        response.raise_for_status()
        if is_bitlink(entered_link, bitlink_header):
            clicks_count = count_clicks(entered_link, bitlink_header)
            print('Количество кликов:', clicks_count)
        else:
            bitlink_result = shorten_link(entered_link, bitlink_header)
            print('Битлинк', bitlink_result)
    except (ConnectionError, MissingSchema, HTTPError):
        print('Incorrect url')


if __name__ == '__main__':
    main()

# https://bit.ly/3JhwFuG
# https://github.com/
