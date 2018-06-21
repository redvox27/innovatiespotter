import requests
from bs4 import BeautifulSoup

class HrefFinder:

    def __init__(self):
        self.url = 'https://www.hdn4food.com/deelnemers/hdn-deelnemers/'
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def get_href_list(self):
        href_list = []
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)

        ankor_list = soup.findAll('a')
        for ankor in ankor_list:
            href = ankor.get('href')
            if 'https://www.hdn4food.com/deelnemers/' == href[:36] and not 'cat-' in href:
                href_list.append(href)

        return list(set(href_list))

hrefFinder = HrefFinder()
hrefFinder.get_href_list()


