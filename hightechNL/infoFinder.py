from bs4 import BeautifulSoup
import requests
from hightechNL.hrefFinder import HrefFinder
import re

class InfoFinder:

    def __init__(self):
        self.href_finder = HrefFinder()
        self.url_list = list(self.href_finder.get_url_list())
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }
        self.info_dict = {}

    def is_postal_code(self, string):
        postal_code = re.search(r'\d{4}? [A-Z]{2}? [A-Z]{1}[a-z]+', string)
        #TODO uitzondering schrijven voor 's-Hertogenbosch

        if postal_code:
            return postal_code.group()
            #return string
        else:
            return None

    def is_street_name(self, string):
        if string[0].isupper() and string[len(string)-1].isdigit() or string[len(string)-2].isdigit():
            split_list = string.split(':')
            if split_list[0] == "Telefoon" or 'Mobiel':
                return False
            return True
        else:
            return False

    def find_website(self, soup):
        paragraph_list = soup.findAll('p')
        website = '-'
        for p in paragraph_list:
            ankor_list = p.findAll('a')
            if ankor_list:
                for ankor in ankor_list:
                    href = ankor.text
                    if href[:3] == 'www':
                        website = href
        return website
    def fill_info_dict(self):
        for url in self.url_list:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            company_name = soup.find('h1').text
            postal_code = '-'
            street = '-'
            website = self.find_website(soup)

            #     text = p.text
            #     text.replace('\n', '')
            #     print(text)
            #     if text:
            #         if self.is_postal_code(text):
            #             postal_code = self.is_postal_code(text)
            #         if self.is_street_name(text):
            #             street = text
            #
            # print(company_name)
            # print(postal_code)
            # print(street)
            # print('\n')

info_finder = InfoFinder()
info_finder.fill_info_dict()