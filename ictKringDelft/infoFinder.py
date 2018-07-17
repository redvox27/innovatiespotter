import requests
from bs4 import BeautifulSoup
from headers import HEADERS
from csvImporter import CsvImporter
from ictKringDelft.hrefFinder import HrefFinder

class InfoFinder:

    def __init__(self):
        self.href_finder = HrefFinder()
        self.url_list = self.href_finder.get_href_list()
        self.headers = HEADERS
        self.importer = CsvImporter('ictKringDelft')

    def find_info(self):
        for url in self.url_list[1:]:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            company_tag = soup.find('h1', {'id': 'tag_pagetitle'})
            if company_tag:
                company = company_tag.text
                print(company)

                adres_tag = soup.find('div', {'id': 'companyadres'})
                if adres_tag:
                    div_list = adres_tag.findChildren('div')
                    adres = div_list[1].text.lstrip().rstrip()
                    postcode = div_list[2].text.lstrip().rstrip()
                    print(adres)
                    print(postcode)
                else:
                    adres = '-'
                    postcode = '-'

                title_string = 'Ga verder naar de website van ' + company
                website_ankor = soup.find('a', {'title': title_string})
                if website_ankor:
                    website = website_ankor.get('href')
                    print(website)
                else:
                    website = '-'
                self.importer.import_to_csv(company, adres, postcode, website)
finder = InfoFinder()
finder.find_info()
