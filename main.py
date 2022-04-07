import requests
import urllib.parse
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")


class IncorrectUrl(Exception):
    """Response status is not 200 OK"""
    pass


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
    return response.json()['link']


def count_clicks(token: str, bitlink: str, unit: str = 'day', units: int = -1) -> int:
    """Count clicks on bitlink"""
    parsed = urllib.parse.urlparse(bitlink)
    bitlink_url = parsed.netloc + parsed.path
    url_clicks_summary = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink_url}/clicks/summary'
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


def is_bitlink(url) -> bool:
    """check url for bitlink"""
    if not requests.get(url).ok:
        raise IncorrectUrl
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc in ('bit.ly', 'bitly.is'):
        return True
    return False


def start():
    """Start program"""
    link = input('Введите ссылку: ')
    try:
        link_booled = is_bitlink(link)
    except IncorrectUrl:
        print('Incorrect link. Response status is not 200 OK')
    else:
        if link_booled:
            try:
                clicks_count = count_clicks(TOKEN, link)
            except (requests.exceptions.HTTPError, NameError):
                print('Incorrect bitlink')
            else:
                print('Количество кликов:', clicks_count)
        else:
            try:
                bitlink_result = shorten_link(TOKEN, link)
            except requests.exceptions.HTTPError:
                print('Incorrect link')
            else:
                print('Битлинк', bitlink_result)


if __name__ == '__main__':
    start()
