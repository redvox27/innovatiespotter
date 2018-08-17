import requests
import re
from bs4 import BeautifulSoup
from headers import HEADERS
from csvImporter import CsvImporter
from fhi.hrefFinder import HrefFinder

class InfoFinder:

    def __init__(self):
        self.finder = HrefFinder()
        self.url_list = self.finder.get_url_list()
        self.importer = CsvImporter('fhi')

    def find_info(self):
        for url in self.url_list:
            req = requests.get(url, HEADERS)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            company = soup.find('h1').text
            print(company)
            block = str(soup.find('div', {'class': 'col-md-4 col-sm-3 col-xs-12'}))
            match = re.search('\d{4}[A-Z]{2}', block)

            if match:
                postcode = match.group()
                self.importer.import_to_csv(company, postcode)

finder = InfoFinder()
finder.find_info()