import requests
import re
from bs4 import BeautifulSoup
from headers import HEADERS
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self, url_tuple_set, file_name):
        self.url_tuple = url_tuple_set
        self.has_contact_set = set()
        self.no_contact_set = set()
        self.importer = CsvImporter(file_name)

    def filter_contact_sets(self):
        print('filtering sets...')
        for company_tuple in self.url_tuple:
            print(company_tuple)
            try:
                req = requests.get(company_tuple[1], HEADERS)
                plain_text = req.text
                soup = BeautifulSoup(plain_text)
                has_contact = False
                ankor_list = soup.findAll('a')
                for ankor in ankor_list:
                    href = ankor.get('href')
                    if href:
                        if ('http' in href and '/contact' in href) or ('http' in href and '/Contact' in href):
                            print(href)
                            print(ankor.text)
                            print('\n')
                            self.has_contact_set.add((company_tuple[0], href))
                            has_contact = True
                        elif '/contact' in href or '/Contact' in href:
                            url = company_tuple[1] + href
                            print(url)
                            print(ankor.text)
                            print('\n')
                            self.has_contact_set.add((company_tuple[0], url))
                            has_contact = True
                        elif href == 'contact.html':
                            url = company_tuple[1] + '/' + href
                            print(url)
                            print(ankor.text)
                            print('\n')
                            self.has_contact_set.add((company_tuple[0], url))
                            has_contact = True
                        elif href == '/contact.html':
                            url = company_tuple[1] + href
                            print(url)
                            print(ankor.text)
                            print('\n')
                            self.has_contact_set.add((company_tuple[0], url))
                            has_contact = True
                        elif ankor.text.lstrip().rstrip() == 'Contact' or ankor.text.lstrip().rstrip() == 'contact' or ankor.text.lstrip().rstrip() == 'CONTACT' or ankor.text.lstrip().rstrip() == '"CONTACT"':
                            if 'http' in href:
                                print(href)
                                print(ankor.text)
                                print('\n')
                                has_contact = True
                                self.has_contact_set.add((company_tuple[0], href))
                            else:
                                url = company_tuple[1] + href
                                print(url)
                                print(ankor.text)
                                print('\n')
                                self.has_contact_set.add((company_tuple[0], url))
                                has_contact = True
                if not has_contact:
                    self.no_contact_set.add(company_tuple)
            except Exception as e:
                print(e)
        print('filtering finished')

    def find_post_code(self, company, url, company_list): #geen goede naam(csv importer)
        try:
            req = requests.get(url, HEADERS)
            plain_text = req.text
            match = re.search('(\d{4}\s[A-Z]{2})|(\d{4}[A-Z]{2})', plain_text)
            if match:
                postcode_string = match.group()
                if len(postcode_string) == 6:
                    postcode = postcode_string[:4] + ' ' + postcode_string[4:]
                    self.importer.import_to_csv(company, postcode)
                self.importer.import_to_csv(company, match.group())
                print('{} found at company_list: {}'.format(match, company_list))
        except Exception as e:
            # print(str(company_list) + ' ' + str(e))
            print(e)

    def find_info(self):
        self.filter_contact_sets()
        for company_list in self.has_contact_set:
            self.find_post_code(company_list[0], company_list[1], company_list)

        for company_list in self.no_contact_set:
            self.find_post_code(company_list[0], company_list[1], company_list)