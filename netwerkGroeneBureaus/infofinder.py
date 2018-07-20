import requests
from bs4 import BeautifulSoup
import re
from headers import HEADERS
from csvImporter import CsvImporter
from netwerkGroeneBureaus.overOnsFinder import OverOnsFinder
from headers import HEADERS

class InfoFinder:

    def __init__(self):
        self.over_ons_finder = OverOnsFinder()
        self.over_ons_url_set = self.over_ons_finder.get_over_ons_url_list()[0]
        self.no_contact_set = self.over_ons_finder.get_over_ons_url_list()[1]


    def find_info(self):
        print('\n')
        for company_set in self.over_ons_url_set:
            try:
                print('companyset: ', company_set)
                company = company_set[0]
                website = company_set[1]
                over_ons_url = company_set[2]
                req = requests.get(over_ons_url, HEADERS)
                plain_text = req.text

                adres_match = re.search('([(A-Z][a-z]+\s[A-Z][a-z]+\s\d+[a-z]| [(A-Z][a-z]+\s[A-Z][a-z]+\s\d+ | [A-Z][a-z]+\s\d+ | [A-Z][a-z]+\s\d+[a-z])', plain_text)
                print(company)
                print(website)
                print(adres_match.groups())
                print('\n')
            except Exception as e:
                print(e)


finder = InfoFinder()
finder.find_info()