import requests
import re
from bs4 import BeautifulSoup
from headers import HEADERS
from hollandSolar.hrefFinder import HrefFinder
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self):
        self.finder = HrefFinder()
        self.url_list = self.finder.get_url_list()
        self.importer = CsvImporter('hollandSolar')

    def find_info(self):
        for url in self.url_list:
            req = requests.get(url, HEADERS)
            html = req.text
            soup = BeautifulSoup(html)

            company = soup.find('h1', {'class': 'ld-title'}).text
            adres_block = soup.find('div', {'class': 'address-block'})
            match = re.search('\d{4}[A-Z]{2}', str(adres_block))
            if match:
                print(company)
                postcode = match.group()
                print(postcode)

                self.importer.import_to_csv(company, postcode)

finder = InfoFinder()
finder.find_info()