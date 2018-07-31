import requests
from bs4 import BeautifulSoup
from headers import HEADERS
from csvImporter import CsvImporter

class HrefFinder:

    def __init__(self):
        self.url = 'http://www.bouwendnederland.nl/lidbedrijven?groupID=4780&page='
        self.headers = HEADERS
        self.url_list = []
        self.fill_url_list()
        self.importer = CsvImporter('bouwendnederland-zuidholland')

    def fill_url_list(self):
        for i in range(1, 8):
            number_string = str(i)
            url = self.url + number_string
            self.url_list.append(url)

    def get_href_list(self):
        for url in self.url_list:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)
            company_list = soup.findAll('div', {'class': 'company'})

            for company in company_list:
                company_name = company.findChild('a').text
                print(company_name)

                bezoekadres = company.findChildren('div', {'class': 'lg-4'})[1].text
                bezoekadres_list = bezoekadres.split('\n')
                postcode = bezoekadres_list[4].replace('\t', '')
                print(postcode)

                self.importer.import_to_csv(company_name, postcode)


finder = HrefFinder()
finder.get_href_list()