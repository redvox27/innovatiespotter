import requests
from bs4 import BeautifulSoup
import csv
from duurzaamgebouwd.hrefFinder import HrefFinder

class InfoFinder:

    def __init__(self):
        self.href_finder= HrefFinder()
        self.url_list = self.href_finder.get_href_list()
        self.headers = self.href_finder.headers

    def import_to_csv(self, company, adres, postcode, website):
        company_dict = {}
        company_dict['company'] = company
        company_dict['adres'] = adres
        company_dict['postcode'] = postcode
        company_dict['website'] = website

        with open('duurzaamgebouwd.csv', 'a') as file:
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

            company = soup.find('h1', {'class': 'title'}).text

            adres = soup.findAll('span', {'itemprop': 'streetAddress'})
            if adres:
                clean_adres = (adres[0].text)
                if 'Postbus' in clean_adres or '+' in clean_adres:
                    clean_adres = '-'
            else:
                clean_adres = '-'
            postalcode = soup.find('span', {'itemprop': 'postalCode'})
            if postalcode:
                clean_postalcode = postalcode.text

            address_locality = soup.find('span', {'itemprop': 'addressLocality'})
            if address_locality:
                clean_locality = address_locality.text
            if postalcode and address_locality:
                finished_postal_code = clean_postalcode + ' ' + clean_locality

            else:
                finished_postal_code = '-'

            website_ankor = soup.findAll('a', {'target': '_blank', 'rel': 'me nofollow'})
            if website_ankor:
                website = website_ankor[len(website_ankor)-1].text
            else:
                website = '-'
            self.import_to_csv(company, clean_adres, finished_postal_code, website)
            print(company)
            print(clean_adres)
            print(finished_postal_code)
            print(website)
            print('\n')

finder = InfoFinder()
finder.find_info()