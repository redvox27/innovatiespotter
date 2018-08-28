import requests
from bs4 import BeautifulSoup
from headers import HEADERS

class HrefFinder:

    def __init__(self):
        self.year = str(2018)
        self.url = 'https://www.buildingholland.nl/partners-{}'.format(self.year)

    def get_url_listI(self):
        req = requests.get(self.url, HEADERS)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)
        url_list = []
        partners = soup.find('ul', {'id': 'partners-{}'.format(self.year)})
        ankor_list = partners.findAll('a')
        for ankor in ankor_list:
            if ankor:
                href = ankor.get('href')
                url = 'https://www.buildingholland.nl' + href
                url_list.append(url)
        return url_list
