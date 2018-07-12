import requests
from bs4 import BeautifulSoup
import csv
from buildingholland.hrefFinder import HrefFinder

class InfoFinder:

    def __init__(self):
        self.href_finder = HrefFinder()
        self.headers = self.href_finder.headers
        self.url_list = self.href_finder.get_href_list()

    def find_info(self):
        for url in self.url_list:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            h1 = soup.find('h1', {'class': 'title'})
            title_span = h1.findChild('span')
            print(title_span)

            print(soup.find('div', {'class': 'text', 'itemprop': 'address'}))
            break

finder = InfoFinder()
finder.find_info()
