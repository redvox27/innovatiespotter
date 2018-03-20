import requests
import csv
from bs4 import BeautifulSoup
import time

class Scraper:

    def __init__(self):
        self.url = 'http://www.weeginstrumenten.nl/leden/'
        self.headers = self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }
        self.company_href_set = set()
        self.company_dict_list = []
        self.fill_company_href_list()


    def fill_company_href_list(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)

        ankor_list = soup.findAll('a')
        for ankor in ankor_list:
            href = ankor.get('href')
            if '/author' in href:
                self.company_href_set.add(href)

    def write_to_csv(self):
        company_list = self.company_dict_list
        print(company_list)
        with open('weeginstrumenten.csv', 'w') as file:
            try:
                headings = (self.company_dict_list[0].keys())
                writer = csv.DictWriter(file, headings, dialect='excel')
                writer.writeheader()
                writer.writerows(company_list)
            except Exception as e:
                print(e)

    def spider(self):
        for url in self.company_href_set:
            company_dict = {}
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            ankor = soup.find('a', {'class': 'website'})
            website = ankor.get('href')
            company_name = soup.find('h3', {'class': 'title'})

            company_dict['company'] = company_name.text
            company_dict['website'] = website

            self.company_dict_list.append(company_dict)

            print(website)
            print(company_name.text)
            print('\n')
        self.write_to_csv()

start = time.time()
s = Scraper()
s.spider()
stop = time.time()
print(stop - start)