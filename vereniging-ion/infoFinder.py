import requests
from bs4 import BeautifulSoup
import csv

class InfoFinder:

    def __init__(self):
        self.url = 'https://www.vereniging-ion.nl/bedrijvenregister?activiteit=&naam=&form_id=ion_bedrijvenregister_bedrijvenregister'
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def import_to_csv(self, company, adres, postcode, website):
        company_dict = {}
        company_dict['company'] = company
        company_dict['adres'] = adres
        company_dict['postcode'] = postcode
        company_dict['website'] = website

        with open('vereniging_ion.csv', 'a') as file:
            try:
                headings = company_dict.keys()
                writer = csv.DictWriter(file, headings)
                writer.writerow(company_dict)
            except Exception as e:
                print(e)

    def findInfo(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)

        company_table_list = soup.findAll('div', {'class': 'bedrijf'})
        for element in company_table_list:
            data_list = element.findChildren('dd')
            if data_list:
                company = element.findChild('h2').text
                straat = data_list[0].text
                postcode = data_list[1].text + data_list[2].text
                website_ankor = data_list[6].find('a')
                if website_ankor:
                    website = website_ankor.get('href')
                else:
                    website = '-'
                print(company)
                print(straat)
                print(postcode)
                print(website)
                self.import_to_csv(company, straat, postcode, website)
            print('\n')
finder = InfoFinder()
finder.findInfo()