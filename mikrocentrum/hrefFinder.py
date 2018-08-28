import requests
from bs4 import BeautifulSoup
from headers import HEADERS

class HrefFinder:

    def __init__(self):
        self.url = 'https://mikrocentrum.nl/high-tech-platform/high-tech-platform-leden/'
        self.headers = HEADERS

    def get_url_list(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)
        url_list = []

        table = soup.find('table', {'class': 'table table-hover deelnemers'})
        deelnemer_list = table.findChildren('td', {'class': 'deelnemer'})

        for deelnemer in deelnemer_list:
            href = deelnemer.findChild('a').get('href')
            url_list.append(href)

        return url_list
