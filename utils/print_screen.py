import os

import random
import re
import string

import cloudscraper
from bs4 import BeautifulSoup as beauty


async def generate_letters(x):
    return ''.join(random.choice(string.ascii_lowercase) for y in range(x))


async def generate_numbers(x):
    return ''.join(str(random.randrange(0, 9)) for y in range(x))


async def generate_url():
    url = "https://prnt.sc/"
    random__letters = await generate_letters(2)
    random__numbers = await generate_numbers(4)
    url += random__letters + random__numbers
    return url


async def get_image():
    try:
        website = await generate_url()

        scraper = cloudscraper.create_scraper(delay=1, browser='chrome')
        scrape = scraper.get(website)

        soup = beauty(scrape.text, "html.parser")
        soup = soup.find('img')

        regx = '(?P<url>https?://[^\\s]+)"'
        img_url = re.search(regx, str(soup)).group("url")
        scrape = scraper.get(img_url)

        soup = beauty(scrape.text, "html.parser")
        if soup.text.__contains__('404 Not Found') or img_url.__contains__('imgur'):
            return await get_image()

        filename = img_url.split('/')[-1]
        path = f"images/{filename}"
        with open(path, 'wb') as f:
            f.write(scrape.content)
        return path

    except AssertionError:
        return await get_image()
    except AttributeError:
        return await get_image()


async def delete_photos():
    files = os.listdir("./images")
    for f in files:
        if f == ".gitkeep":
            continue
        os.remove(f"images/{f}")
