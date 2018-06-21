import csv

import requests
from bs4 import BeautifulSoup
from hdn4food.hrefFinder import HrefFinder

class InfoFinder:

    def __init__(self):
        self.hrefFinder = HrefFinder()
        self.href_list = self.hrefFinder.get_href_list()

        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def write_to_csv(self, company_dict):

        try:
            with open('hdn4food.csv', 'a') as file:
                try:
                    headings = company_dict.keys()
                    writer = csv.DictWriter(file, headings)
                    writer.writerow(company_dict)
                except Exception as e:
                    print(e)
        except Exception as e:
            print('exception: {}'.format(e))

    def find_info(self):
        for href in self.href_list:
            req = requests.get(href, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)
            company = soup.find('h1').text
            print(company)
            table = soup.find('div', {'class': 'content-right fr'})
            if table:
                company_dict = {}
                paragraphs = table.findChildren('p')
                paragraph = str(paragraphs[1])
                adres_list = paragraph.split('<br/>')

                company_dict['bedrijf'] = company
                adres = adres_list[0].replace('<p>', '')
                company_dict['adres'] = adres
                postcode = adres_list[1].rstrip().lstrip()
                company_dict['postcode'] = postcode
                self.write_to_csv(company_dict)


info = InfoFinder()
info.find_info()