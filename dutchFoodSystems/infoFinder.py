import csv

import requests
from bs4 import BeautifulSoup
from dutchFoodSystems.hrefFinder import HrefFinder

class InfoFinder:

    def __init__(self):
        self.href_finder = HrefFinder()
        self.href_list = self.href_finder.get_href_list()
        self.headers = self.href_finder.headers

    def scrape_content_richt(self, content_right):
        br_list = content_right.findChildren('br')
        text_list = []
        for br in br_list:
            text = br.nextSibling
            try:
                clean_text = text.lstrip().rstrip().replace('\n', '')
                if clean_text != '':
                    text_list.append(clean_text)
            except Exception:
                continue

        return text_list

    def get_website(self, soup):
        ankor_list = soup.findAll('a')
        return(ankor_list[2].get('href'))

    def import_to_csv(self, company, adres, postcode, website):
        company_dict = {}
        company_dict['company'] = company
        company_dict['adres'] = adres
        company_dict['postcode'] = postcode
        company_dict['website'] = website

        with open('dutchFoodSystems.csv', 'a') as file:
            try:
                headings = company_dict.keys()
                writer = csv.DictWriter(file, headings)
                writer.writerow(company_dict)
            except Exception as e:
                print(e)
        #todo write to csv copy pasta
    def find_info(self):
        for url in self.href_list:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)
            content_right = soup.find('div', {'id': 'contentright'})

            company_text = soup.find('div', {'class': 'blue'}).text
            company_name = company_text.rstrip().lstrip()
            print(company_name)

            text_list = self.scrape_content_richt(content_right)
            if text_list:
                adres = text_list[0]
                postcode = text_list[1]
                website = self.get_website(content_right)
                self.import_to_csv(company_name, adres, postcode, website)
                print('adres: {}'.format(adres))
                print('postcode: {}'.format(postcode))
                print('website: {}'.format(website))
            print('\n')

info_finder = InfoFinder()
info_finder.find_info()