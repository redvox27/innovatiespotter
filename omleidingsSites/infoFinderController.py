import requests
import re
from bs4 import BeautifulSoup
from headers import HEADERS
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self, url_tuple):
        self.url_tuple = url_tuple
        self.has_contact_set = set()
        self.no_contact_set = set()

    def filter_contact_sets(self):
        print('filtering sets...')
        for company_tuple in self.url_tuple:
            try:
                req = requests.get(company_tuple[1], HEADERS)
                plain_text = req.text
                soup = BeautifulSoup(plain_text)

                ankor_list = soup.findAll('a')
                for ankor in ankor_list:
                    href = ankor.get('href')
                    if href:
                        if ('http' in href and '/Contact' in href) or ('http' in href and '/contact' in href):
                            self.has_contact_set.add((company_tuple[0], href, 'if', '0'))
                        elif ('http' in href and 'Contact' in href) or ('http' in href and 'contact' in href):
                            self.has_contact_set.add((company_tuple[0], '/' + href, 'elif', '1'))
                        elif '/Contact' in href or '/contact' in href:
                            over_ons_url = company_tuple[1] + href
                            self.has_contact_set.add((company_tuple[0], over_ons_url, 'elif', '2'))
                        elif 'Contact' in href or 'contact' in href:
                            over_ons_url = company_tuple[1] + '/' + href
                            self.has_contact_set.add((company_tuple[0], over_ons_url, 'elif', '3'))

                        else:
                            self.no_contact_set.add(company_tuple)
            except Exception as e:
                print(e)
        print('filtering finished')

    def find_info(self):
        self.filter_contact_sets()
        for company_list in self.has_contact_set:
            print(company_list)