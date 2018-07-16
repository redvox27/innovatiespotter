import requests
from bs4 import BeautifulSoup
from headers import HEADERS
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self):
        self.url = 'https://nvvgt.nl/bedrijfsleden'
        self.headers = HEADERS
        self.importer = CsvImporter('nvvgt')

    def find_info(self):
        req = requests.get(self.url, self.headers)
        plain_text =req.text
        soup = BeautifulSoup(plain_text)

        info_table = soup.findAll('div', {'class': 'col-lg-3 col-md-3 col-sm-3 col-xs-12'})

        for element in info_table:
            ankor = element.findChild('a')
            website = ankor.get('href')
            company = ankor.get('title')

            adres_string = element.findChild('div', {'class': 'hentry__content'}).text.lstrip().rstrip()
            print(adres_string)
            splitted_adres_string = adres_string.split('\n')
            adres = splitted_adres_string[0].replace('\r', '')
            postcode = splitted_adres_string[1].replace('\t', '').replace('\r', '')
            print(adres)
            print(postcode)

            self.importer.import_to_csv(company, adres, postcode, website)

finder = InfoFinder()
finder.find_info()