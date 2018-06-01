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

    def get_postal_code(self, string, postal_code):
        match = re.search(r'\d{4}\s[A-Z]{2}\s[A-Z]{1}[a-z]+', string)
        if match:
            return str(match.group())
        else:
            return postal_code

    def get_street_name(self, string, street):
        match = re.search(r'[A-Z]{1}[a-z]+\s\d+', string)
        if match and match.group() != 'Verken 11' and match.group()[:7] != 'Postbus':
            return str(match.group())
        else:
            return street

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

    def get_dict_list(self):
        dict_list = []

        for url in self.url_list:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            company_name = soup.find('h1').text
            street = '-'
            postal_code = '-'
            website = self.find_website(soup)
            paragraph_list = soup.findAll('p')
            for p in paragraph_list:
                text = p.text
                if text:
                    postal_code = self.get_postal_code(text, postal_code)
                    street = self.get_street_name(text, street)
            dict_list.append({'company_name': company_name, 'postal_code': postal_code, 'website': website})

        return dict_list