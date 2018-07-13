import requests
from bs4 import BeautifulSoup
from metaalgieterijen.hrefFinder import HrefFinder
import csv

class InfoFinder:

    def __init__(self):
        self.href_finder = HrefFinder()
        self.url_list = self.href_finder.get_href_list()
        self.headers = self.href_finder.headers

    def import_to_csv(self, company, adres, postcode, website):
        company_dict = {}
        company_dict['company'] = company
        company_dict['adres'] = adres
        company_dict['postcode'] = postcode
        company_dict['website'] = website

        with open('metaalgieterijen.csv', 'a') as file:
            try:
                headings = company_dict.keys()
                writer = csv.DictWriter(file, headings)
                writer.writerow(company_dict)
            except Exception as e:
                print(e)

    def find_info(self):
        for url in self.url_list:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)
            table = soup.find('table', {'style': 'border-collapse: collapse; width: 601px; height: 524px;'})
            if table:
                print(url)
                rows = table.findChildren('tr')
                company_string = rows[0].text.lstrip().rstrip()
                split_company_string_list = company_string.split('Bedrijfsnaam')
                company = split_company_string_list[1].replace('\n', '').replace('\r', '')
                print(company)

                adres_row = rows[1]
                adres_data = (adres_row.findChildren('td'))
                adres = adres_data[1].text.lstrip().rstrip()
                print(adres)

                postcode = rows[2].text.lstrip().rstrip()
                print('postcode: ' + postcode)

                ankor_list = soup.findAll('a')
                website = ankor_list[len(ankor_list)-2].get('href')
                print(website)
                self.import_to_csv(company, adres, postcode, website)
                print('\n')

finder = InfoFinder()
finder.find_info()