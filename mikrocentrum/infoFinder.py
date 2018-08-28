import requests
import re
from bs4 import BeautifulSoup
from headers import HEADERS
from mikrocentrum.hrefFinder import HrefFinder
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self):
        self.finder = HrefFinder()
        self.importer = CsvImporter('mikrocentrum3')
        self.headers = HEADERS

    def get_url_list(self):
        return self.finder.get_url_list()

    def extract_postcode_from_String(self, string):
        try:
            splitted_string = string.split('\xa0')
            postcode = splitted_string[0] + splitted_string[1]
            return postcode.lstrip().rstrip()
        except:
            return

    def find_info(self):
        for url in self.get_url_list():
            req = requests.get(url, self.headers,verify=False)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            company_string = soup.find('div', {'id': 'Ititle1'})
            if company_string:
                company = company_string.text.lstrip().rstrip()
                print(company)
                table = str(soup.find('div', {'id': 'head'}))
                match_list = re.findall('\d{4}\s[A-Z]{2}', table)
                if len(match_list) == 1:
                    postcode_string = match_list[0]
                    postcode = self.extract_postcode_from_String(postcode_string)
                    if postcode:
                        self.importer.import_to_csv(company, postcode)
                if len(match_list) == 2:
                    postcode_string = match_list[1]
                    postcode = self.extract_postcode_from_String(postcode_string)
                    if postcode:
                        self.importer.import_to_csv(company, postcode)

finder = InfoFinder()
finder.find_info()