import requests
import re
from bs4 import BeautifulSoup
from headers import HEADERS
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self):
        self.url = 'http://vvem.nl/leden/'
        self.importer = CsvImporter('vvem')

    def find_info(self):
        req = requests.get(self.url, HEADERS)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)

        leden_list = soup.findAll('article', {'class': 'leden organisatie '})
        count = 0
        for lid in leden_list:
            company_text = lid.findChild('h3', {'class': 'name'})
            if company_text:
                company = company_text.text
                match = re.search('\d{4}\s[A-Z]{2}', str(lid))
                if match:
                    count += 1
                    postcode = match.group()
                    print(company)
                    print(postcode)
                    self.importer.import_to_csv(company, postcode)
                    print('\n')

finder = InfoFinder()
finder.find_info()