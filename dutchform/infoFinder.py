import requests
from bs4 import BeautifulSoup
from dutchform.hrefFinder import HrefFinder
from csvImporter import CsvImporter
from headers import HEADERS

class InfoFinder:

    def __init__(self):
        self.href_finder = HrefFinder()
        self.url_list = self.href_finder.get_href_list()
        self.headers = HEADERS
        self.importer = CsvImporter('dutchform')


    def get_adres_and_postcode(self, soup):
        p_list = soup.findAll('p')
        adres_p = str(p_list[1])
        splitted_paragraph = adres_p.split('>')
        adres = splitted_paragraph[1].lstrip().rstrip().replace('<br/', '')
        postcode = splitted_paragraph[2].lstrip().rstrip().replace('<br/', '')
        return adres, postcode

    def find_info(self):
        for url in self.url_list:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)
            href_list = []

            company = soup.find('h1').text
            print(company)

            adres, postcode = self.get_adres_and_postcode(soup)
            print(adres, ' ', postcode)

            ankor_list = soup.findAll('a')
            for ankor in ankor_list:
                href = ankor.get('href')
                if not 'dutchform' in href:
                    href_list.append(href)
            website = href_list[5]
            print(website)
            self.importer.import_to_csv(company, adres, postcode, website)

finder = InfoFinder()
finder.find_info()
