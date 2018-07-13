import requests
from bs4 import BeautifulSoup
import csv
import re

from mtRanglijsten.hrefFinder import HrefFinder

class InfoFinder:

    def __init__(self):
        self.href_finder = HrefFinder()
        self.url_list = self.href_finder.get_href_list()
        self.headers = self.href_finder.headers

    def find_plaats(self, inner_content_paragraph):
        plaats_list = re.findall(pattern=r"([A-Z]{1}[a-z]+|'s\s[A-Z]{1}[a-z]+)", string=(str(inner_content_paragraph)))
        match_string = ''.join(plaats_list)
        split_match_string = match_string.split('Plaats')
        try:
            search_string = split_match_string[1]
            if search_string:
                plaats = re.search(pattern=r"([A-Z]{1}[a-z]+|'\D[A-Z]{1}[a-z]+)", string=search_string)
                return plaats.group()
            else:
                return '-'
        except:
            return '-'

    def find_omzet(self, paragraph):
        split_paragraph = paragraph.split('Omzet 2016')
        try:
            second_split = split_paragraph[1]
            omzet = re.search(pattern=r'\d+', string=second_split)
            if omzet:
                return int(omzet.group() + '000000')
            else:
                return '-'
        except:
            return '-'
    def find_fte(self, paragraph):
        split_paragraph = paragraph.split('FTE')
        try:
            second_split = split_paragraph[1]
            fte = re.search(pattern=r'\d+', string=second_split)
            if fte:
                return float(fte.group())
            else:
                return '-'
        except:
            return '-'

    def import_to_csv(self, company, ceo, plaats, omzet_2016, fte):
        company_dict = {}
        company_dict['company'] = company
        company_dict['ceo'] = ceo
        company_dict['plaats'] = plaats
        company_dict['omzet2016'] = omzet_2016
        company_dict['fte'] = fte

        with open('mtRanglijsten.csv', 'a') as file:
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

            title = soup.find('h1', {'class': 'title_single'}).text
            split_title = title.split('.')
            company = split_title[1].rstrip().lstrip()
            print(company)

            inner_content = soup.find('section', {'class': 'inner_content bg-white padding-sm'})
            inner_content_paragraph = str(inner_content.findChild('p'))
            #print(inner_content_paragraph)
            try:
                CEO = re.search(pattern=r'[A-Z]{1}[a-z]+\s([A-Z]{1}[a-z]+|[a-z]+\s[A-Z]{1}[a-z]+|[a-z]+\s[a-z]+\s[A-Z]{1}[a-z]+)'
                                , string=str(inner_content_paragraph)).group()
            except:
                CEO = '-'

            plaats = self.find_plaats(inner_content_paragraph)
            omzet2016 = self.find_omzet(inner_content_paragraph)
            fte = self.find_fte(inner_content_paragraph)

            self.import_to_csv(company, CEO, plaats, omzet2016, fte)

            print('CEO: ' + CEO)
            print('plaats: ' + plaats)
            print('omzet 2016: ' + str(omzet2016))
            print('fte: ' + str(fte))
            print('\n')
finder = InfoFinder()
finder.find_info()