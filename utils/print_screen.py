import os

import random
import re
import string

import cloudscraper
from bs4 import BeautifulSoup as beauty


def generate_letters(x):
    return ''.join(random.choice(string.ascii_lowercase) for y in range(x))


def generate_numbers(x):
    return ''.join(str(random.randrange(0, 9)) for y in range(x))


def generate_url():
    url = "https://prnt.sc/"
    random__letters = generate_letters(2)
    random__numbers = generate_numbers(4)
    url += random__letters + random__numbers
    return url


def get_image():
    try:
        website = generate_url()

        scraper = cloudscraper.create_scraper(browser='chrome')
        scrape = scraper.get(website)

        soup = beauty(scrape.text, "html.parser")
        soup = soup.find('img')

        regx = '(?P<url>https?://[^\\s]+)"'
        img_url = re.search(regx, str(soup)).group("url")
        scrape = scraper.get(img_url)

        if scrape.headers.get("Content-Type") == 'text/html' or scrape.headers.get("Content-Length") == '503':
            return get_image()

        soup = beauty(scrape.text, "html.parser")
        filename = img_url.split('/')[-1]
        path = f"images/{filename}"
        with open(path, 'wb') as f:
            f.write(scrape.content)
        return path, img_url

    except AssertionError:
        return get_image()
    except AttributeError:
        return get_image()


async def delete_photos():
    files = os.listdir("./images")
    for f in files:
        if f == ".gitkeep":
            continue
        os.remove(f"images/{f}")
