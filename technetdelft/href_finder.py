import requests
from bs4 import BeautifulSoup
from headers import HEADERS

class HrefFinder:

    def __init__(self):
        self.url = 'https://www.technetdelft.nl/leden'
        self.headers = HEADERS

    def get_href_list(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)

        href_list = []

        ankor_list = soup.findAll('a')
        for ankor in ankor_list:
            href = ankor.get('href')
            if href:
                if '/leden/' in href:
                    url = 'https://www.technetdelft.nl' + href
                    href_list.append(url)
        return list(set(href_list))
