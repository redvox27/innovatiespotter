import csv

import requests
from bs4 import BeautifulSoup

from js.teqnow.hrefFinder import HrefFinder


class InfoFinder:

    def __init__(self):
        self.hrefFinder = HrefFinder()
        self.href_list = self.hrefFinder.get_href_list()
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def scrape_table(self, soup, company):
        company_dict = {}
        table = soup.findChild('table')
        rows = table.findChildren('tr')

        company_dict['bedrijf'] = company

        adres_row = rows[0]
        adres = adres_row.findChildren('td')[1].text
        company_dict['adres'] = adres
        print(adres)

        postcode_row = rows[1]
        postcode = postcode_row.findChildren('td')[1].text
        company_dict['postcode'] = postcode
        print(postcode)

        website_row = rows[5]
        website = website_row.findChildren('td')[1].text
        company_dict['website'] = website
        print(website)

        contact_persoon_row = rows[6]
        contact_persoon = contact_persoon_row.findChildren('td')[1].text
        company_dict['contactpersoon'] = contact_persoon
        print(contact_persoon)

        contact_persoon_email_row = rows[7]
        contact_persoon_email = contact_persoon_email_row.findChildren('td')[1].text
        company_dict['contactpersoon_mail'] = contact_persoon_email
        print(contact_persoon_email)
        return company_dict

    def find_info(self):
        for url in self.href_list:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            try:
                company = soup.find('h1', {'class': 'edn_articleTitle'}).text
                print(company)

                company_dict = self.scrape_table(soup, company)
                with open('teqnow.csv', 'a') as file:
                    try:
                        headings = company_dict.keys()
                        writer = csv.DictWriter(file, headings)
                        writer.writerow(company_dict)
                    except Exception as e:
                        print(e)
            except Exception as e:
                print('exception: {}'.format(e))
