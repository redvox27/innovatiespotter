import requests
import re
from bs4 import BeautifulSoup
from headers import HEADERS
from buildingholland.hrefFinder import HrefFinder
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self):
        self.finder = HrefFinder()
        self.url_list = self.finder.get_url_listI()
        self.importer = CsvImporter('buildingholland')

    def find_info(self):
        for url in self.url_list:
            req = requests.get(url, HEADERS)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            try:
                company = soup.find('h1', {'class': 'title'}).text
                postcode = soup.find('span', {'itemprop': 'postalCode'}).text
                print(company)
                print(postcode)
                self.importer.import_to_csv(company, postcode)
            except Exception as e:
                print('exception: {} occured at url: {}'.format(e, url))

finder = InfoFinder()
finder.find_info()