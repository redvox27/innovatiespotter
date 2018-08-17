import requests
from bs4 import BeautifulSoup
from headers import HEADERS

class HrefFinder:

    def __init__(self):
        self.url = 'https://fhi.nl/ledenlijst/?page='
        self.initonal_url_list = []
        self.fill_list()

    def fill_list(self):
        for i in range(1, 22):
            page_number = str(i)
            url = self.url + page_number
            self.initonal_url_list.append(url)

    def get_url_list(self):
        url_list = []
        for url in self.initonal_url_list:
            req = requests.get(url, HEADERS)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            content = soup.find('div', {'class': 'panel-group'})
            ankor_list = content.findChildren('a')
            for ankor in ankor_list:
                if ankor:
                    href = ankor.get('href')
                    if href:
                        url = 'http://fhi.nl' + href
                        url_list.append(url)

        return url_list
