import csv

import requests
from bs4 import BeautifulSoup
from dptech.hrefFinder import HrefFinder

class InfoFinder:

    def __init__(self):
        self.href_finder = HrefFinder()
        self.href_list = self.href_finder.get_href_list()
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def get_company(self, href):
        split_href = href.split('/leden/')
        company_string = (split_href[1])
        company_string = company_string.replace('/', '')
        company = company_string.replace('-', ' ')
        return company

    def write_to_csv(self, company_dict):

        try:
            with open('dptech.csv', 'a') as file:
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
            company_dict = {}

            company = self.get_company(href)
            company_dict['bedrijf'] = company

            data_box = soup.find('div', {'class': 'box fr bg_white leden_right'})

            if data_box:
                li_list = data_box.findChildren('li')

                adres = li_list[0].text
                company_dict['adres'] = adres
                print(adres)
                postcode = li_list[1].text
                company_dict['postcode'] = postcode
                print(postcode)
                website = li_list[5].find('a').get('href')
                company_dict['website'] = website
                print(website)
                self.write_to_csv(company_dict)


finder = InfoFinder()
finder.find_info()

