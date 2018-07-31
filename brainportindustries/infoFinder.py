import requests
from bs4 import BeautifulSoup
from headers import HEADERS
from brainportindustries.hrefFinder import HrefFinder
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self):
        self.finder = HrefFinder()
        self.url_list = self.finder.get_href_list()
        self.importer = CsvImporter('brainportindustries')
        self.headers = HEADERS

    def find_info(self):
        for url in self.url_list:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)
            try:
                company = soup.find('h1').text
                postcode = soup.find('span', {'class': 'postcode'}).text
                self.importer.import_to_csv(company, postcode)
                print(postcode)
                print(company)


            except Exception as e:
                print('exception occured at url: {} error: {}'.format(url, e))
finder = InfoFinder()
finder.find_info()