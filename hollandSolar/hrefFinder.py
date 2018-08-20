import requests
from bs4 import BeautifulSoup
from headers import HEADERS

class HrefFinder:

    def __init__(self):
        self.url = 'https://hollandsolar.nl/leden'

    def get_url_list(self):
        req = requests.get(self.url, HEADERS)
        html = req.text
        soup = BeautifulSoup(html)
        url_list = []

        row = soup.find('div', {'class': 'brand-block'})
        medium_list = row.findChildren('div', {'class': 'brand-td'})

        for medium in medium_list:
            ankor = medium.findChild('a')
            if ankor:
                href = ankor.get('href')
                if href:
                    url = 'https://hollandsolar.nl' + href
                    url_list.append(url)
        return url_list
