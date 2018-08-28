import requests
import re
from bs4 import BeautifulSoup
from headers import HEADERS
from js.mkbtop100.hrefFinder import HrefFinder
from csvImporter import CsvImporter


class InfoFinder:

    def __init__(self):
        self.finder = HrefFinder()
        self.url_list = self.finder.get_url_list()
        self.importer = CsvImporter('mbktop100_2008')
        self.headers = HEADERS

    def find_info(self):
        for url in self.url_list:
            req = requests.get(url)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            content = soup.find('div', {'class': 'cpcontent'})
            try:
                company = content.findChild('h2').text
                postcode = re.search('\d{4}\s[A-Z]{2}', str(content)).group()
                print(company)
                self.importer.import_to_csv(company, postcode)
            except Exception as e:
                print('exception: {} found at url: {}'.format(e, url))


finder = InfoFinder()
finder.find_info()
