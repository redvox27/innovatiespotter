import requests
from bs4 import BeautifulSoup

class HrefFinder:

    def __init__(self):
        self.url = 'https://www.mt.nl/lijst/de-maakindustrie-100-van-2017'
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def get_soup(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)
        return soup

    def get_href_list(self):
        soup = self.get_soup()
        href_list = []
        ankor_list = soup.findAll('a')

        for ankor in ankor_list:
            href = ankor.get('href')
            if href:
                if '/de-maakindustrie-100-van-2017/' in href:
                    href_list.append(href)
        return sorted(list(set(href_list)))
