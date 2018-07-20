import requests
from bs4 import BeautifulSoup
from headers import HEADERS

class UrlFinder:

    def __init__(self):
        self.url = 'https://www.netwerkgroenebureaus.nl/brancheorganisatie/ledenlijst'
        self.headers = HEADERS

    def get_url_list(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)
        url_list = []

        table = soup.find('table', {'cellspacing': '0'})
        ankor_list = table.findChildren('a')
        for ankor in ankor_list:
            href = ankor.get('href')
            company = ankor.text
            if href:
                url_list.append((company, href))

        return url_list

