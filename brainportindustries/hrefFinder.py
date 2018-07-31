import requests
from bs4 import BeautifulSoup
from headers import HEADERS

class HrefFinder:

    def __init__(self):
        self.url = 'https://www.brainportindustries.com/nl/ledenoverzicht'
        self.headers = HEADERS

    def get_href_list(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)
        url_list = []

        item_list = soup.findAll('div', {'class', 'faces-item'})
        for item in item_list:
            href = item.findChild('a').get('href')
            url = 'https://www.brainportindustries.com' + href
            url_list.append(url)
        return url_list
