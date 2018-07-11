import requests
from bs4 import BeautifulSoup
import csv
from tfhc.hrefFinder import HrefFinder

class InfoFinder:

    def __init__(self):
        self.href_finder = HrefFinder()
        self.headers = self.href_finder.headers
        self.href_list = self.href_finder.get_href_list()

    def import_to_csv(self, company, adres, postcode, website):
        company_dict = {}
        company_dict['company'] = company
        company_dict['adres'] = adres
        company_dict['postcode'] = postcode
        company_dict['website'] = website

        with open('tfhc.csv', 'a') as file:
            try:
                headings = company_dict.keys()
                writer = csv.DictWriter(file, headings)
                writer.writerow(company_dict)
            except Exception as e:
                print(e)

    def find_info(self):
        for href in self.href_list:
            req = requests.get(href, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            company = soup.find('h1', {'class': 'entry-title'}).text
            print(company)
            info_table = str(soup.find('div', {'style': 'float: left; display: inline; margin-bottom:20px;'}))
            split_info = info_table.split('<br/>')
            adres = split_info[1].lstrip().rstrip()
            postcode = split_info[2].lstrip().rstrip()
            website_ankor = soup.find('a', {'class': 'fusion-button button-flat button-round button-xlarge button-default button-1'})
            if website_ankor:
                website = website_ankor.get('href')
            else:
                website = '-'
            self.import_to_csv(company, adres, postcode, website)
            print('\n')

finder = InfoFinder()
finder.find_info()

