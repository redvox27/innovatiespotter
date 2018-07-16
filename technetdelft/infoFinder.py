import requests
from bs4 import BeautifulSoup
from headers import HEADERS
from csvImporter import CsvImporter as importer
from technetdelft.href_finder import HrefFinder

class InfoFinder:

    def __init__(self):
        self.href_finder = HrefFinder()
        self.url_list = self.href_finder.get_href_list()
        self.headers = HEADERS
        self.importer = importer('technetDelft')

    def find_info(self):
        for url in self.url_list:
            print(url)
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            company = soup.find('h1').text.lstrip().rstrip()

            adres_li = soup.find('li', {'class': 'visitAddress'})
            if adres_li:
                span = adres_li.findChild('span', {'class': 'value'}).text
                split_span = span.split('\n')
                adres = split_span[1].lstrip().rstrip()
                postcode = split_span[2].replace('Nederland', '').replace('NL', '').replace('Netherlands', '').lstrip().rstrip()

                website_li = soup.find('li', {'class': 'url'})
                if website_li:
                    website = website_li.findChild('a').get('href')

                else:
                    website = '-'
                self.importer.import_to_csv(company, adres, postcode, website)


finder = InfoFinder()
finder.find_info()