import requests
from bs4 import BeautifulSoup
from automotive.hrefFinder import HrefFinder
from headers import HEADERS
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self):
        self.finder = HrefFinder()
        self.headers = HEADERS
        self.importer = CsvImporter('automotive')

    def find_info(self):
        url_list = self.finder.get_href_list()
        for url in url_list[:-1]:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)
            print('infoFinder_url: ', url)

            detail_entry = soup.find('div', {'class':'spDetailEntry'})
            if detail_entry:
                try:
                    company = detail_entry.findChild('h1').text
                    print(company)

                    adres_div = detail_entry.findChild('div', {'class': 'spClassViewInbox street'})
                    adres = adres_div.findChild('span').text
                    print(adres)

                    postcode_div = detail_entry.findChild('div', {'class': 'spClassViewInbox postcode'})
                    postcode = postcode_div.findChild('span').text
                    print(postcode)

                    website_div = detail_entry.findChild('div',{'class': 'spClassViewUrl website'})
                    if website_div:
                        website = website_div.findChild('a').get('href')
                    else:
                        website = '-'
                    print(website)
                    self.importer.import_to_csv(company, adres, postcode, website)
                except Exception as e:
                    print('exception found: ' + str(e))
                    print('exception_url: ' + url)
            print('\n')

finder = InfoFinder()
finder.find_info()