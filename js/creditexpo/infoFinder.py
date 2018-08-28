import requests
import re
from bs4 import BeautifulSoup
from headers import HEADERS
from js.creditexpo.hrefFinder import HrefFinder
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self):
        self.finder = HrefFinder()
        self.url_list = self.finder.get_url_list()
        self.importer = CsvImporter('creditexpo')
        self.headers = HEADERS

    def find_info(self):
        for url in self.url_list:
            print(url)
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            table = soup.find('table')
            if table:
                try:
                    rows = table.findChildren('tr')
                    for row in rows:
                        th = row.findChild('th').text
                        if th == 'Bedrijfsnaam':
                            company = row.findChild('td').text
                            print(company)
                        if th == 'Postcode':
                            postcode = row.findChild('td').text
                            print(postcode)
                    self.importer.import_to_csv(company, postcode)
                except Exception as e:
                    print('exception: {} occured at url: {}'.format(e, url))
finder = InfoFinder()
finder.find_info()