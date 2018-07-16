import requests
from bs4 import BeautifulSoup
from headers import HEADERS

class HrefFinder:

    def __init__(self):
        self.url = 'http://www.dutchform.nl/leden/leden/'
        self.headers = HEADERS

    def replace_all(self, text):
        replace_dict = {' ': '-', '/': '-', 'B.V.': 'b-v', '.': '-'}

        for i, j in replace_dict.items():
            text = text.replace(i, j)
        return text

    def get_href_list(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)

        ankor_list = soup.findAll('a')
        href_list = []

        for ankor in ankor_list:
            href = ankor.get('href')
            if href:
                if '/leden/leden' in href:
                    href_list.append(href)
        return href_list[11:-13]
