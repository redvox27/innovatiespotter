import requests
from bs4 import BeautifulSoup
from headers import HEADERS

class HrefFinder:

    def __init__(self):
        self.headers = HEADERS
        self.url = 'https://www.ictkring-delft.nl/page3741/deelnemers/dv/listpage'
        self.url_list = []
        self.fill_url_list()


    def fill_url_list(self):
        for i in range(1, 7):
            url = self.url + str(i)
            self.url_list.append(url)

    def get_href_list(self):
        href_list = []
        for url in self.url_list:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            ankor_list = soup.findAll('a')
            for ankor in ankor_list:
                href = ankor.get('href')
                if href:
                    if '/bedrijf' in href:
                        href_list.append(href)
        return href_list
