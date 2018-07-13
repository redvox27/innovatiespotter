import requests
from bs4 import BeautifulSoup
import csv
import re

class InfoFinder:

    def __init__(self):
        self.url = 'http://www.avneg.nl/Leden.aspx?NL-1-234-0'
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def import_to_csv(self, company, postcode, website):
        company_dict = {}
        company_dict['company'] = company
        company_dict['postcode'] = postcode
        company_dict['website'] = website

        with open('avneg.csv', 'a') as file:
            try:
                headings = company_dict.keys()
                writer = csv.DictWriter(file, headings)
                writer.writerow(company_dict)
            except Exception as e:
                print(e)

    def find_info(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)

        table = soup.find('table', {'align': 'left'})
        rows = table.findChildren('tr')
        for row in rows:
            table_data = row.findChildren('td')
            value_string = str(table_data[1])
            split_values = value_string.split('>')
            company = split_values[1].replace('<br/', '')
            postcode = split_values[3].replace('<br/', '')
            website_string = split_values[4]
            print(website_string)
            website_match = re.search("[w]{3}\D[a-z]+\D([nl]{2}|[com]{3}|[biz]{3})", website_string)
            print(website_match)
            if website_match:
                website = website_match.group()
            else:
                website = '-'

            self.import_to_csv(company, postcode, website)

            print('\n')
finder = InfoFinder()
finder.find_info()