import requests
import time
import re
from bs4 import BeautifulSoup
from headers import HEADERS
from csvImporter import CsvImporter
from driedprintatlas.hrefFinder import HrefFinder

class infoFinder:

    def __init__(self):
        self.finder = HrefFinder()
        self.url_list = self.finder.get_url_list()
        self.headers = HEADERS
        self.importer = CsvImporter('3dprintatlas')

    def find_info(self):
        for url in self.url_list:
            try:
                soup = BeautifulSoup(requests.get(url, self.headers).text)
                name = soup.find('div', {'class': 'field-title'}).text
                postcode = soup.find('span', {'class': 'postal-code'})
                match = re.search('\d{4}\s[A-Z]{2}', postcode)
                if match:
                    postcode = match.group()
                    print(url)
                    print(name)
                    print(postcode)
            except ConnectionError as e:
                print(e)
                time.sleep(5)
finder = infoFinder()
finder.find_info()