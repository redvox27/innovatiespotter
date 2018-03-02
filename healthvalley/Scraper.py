import requests
from bs4 import BeautifulSoup
import csv
import collections

class Scraper():


    def __init__(self):
        self.url = 'https://www.healthvalley.nl/netwerk/partners'
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

        self.href_list = []
        self.company_list =[]

    def get_url(self):
        return self.url

    def fill_href_set(self, panel_body):
        href_set = set()

        for panel in panel_body:
            ankor = panel.findAll('a')

            for href in ankor:
                full_href = 'https://www.healthvalley.nl' + href.get('href')
                href_set.add(full_href)

        self.href_list = list(href_set)

    def spider(self):
        url = self.get_url()
        request = requests.get(url, self.headers)
        plain_text = request.text
        soup = BeautifulSoup(plain_text)

        panel_body = soup.findAll('div', attrs={'class': 'tab-content'})
        self.fill_href_set(panel_body)

        self.crawl_page()
        self.correct_company_dict()
        self.write_to_csv()

    def crawl_page(self):
        for i in range(1, 2):
            url = self.href_list[i]
            print("new url being processed...")
            request = requests.get(url, self.headers)
            plain_text = request.text
            soup = BeautifulSoup(plain_text)

            table = soup.find('table', attrs={'class' : 'c-table c-table--oddeven'})

            table_body = table.find('tbody')

            rows = table_body.findAll('tr')

            temp_dict = {}

            for column in rows:
                try:
                    table_header = column.find('th').text
                    table_header = table_header.replace(':', '')
                    table_header = table_header.replace('\u2002', '')
                    table_header = table_header.replace('\ufffd', '')
                    table_data = column.find('td').text
                    table_data = table_data.replace('\u2002', '')
                    table_data = table_data.replace('\ufffd', '')

                    temp_dict[table_header] = table_data

                except Exception as e:
                    print(e)

            self.company_list.append(temp_dict)


    def correct_company_dict(self):
        for dictionary in self.company_list:

            key_list = list(dictionary.keys())
            temp_key_list = []
            value_list = []

            for key in key_list:
                if key == 'Organisatietype' or key == 'Specialisatie' or key == 'E-mail':
                    temp_key_list.append(key)

                    value_list.append(dictionary[key])

            print('key_list: ' + str(key_list))
            print('temp_key_list: ' + str(temp_key_list))
            print('value_list: ' + str(value_list))

            if 'Organisatietype' not in temp_key_list:
                dictionary['Organisatietype'] = 'Niet bekend'
                temp_key_list.append('Organisatietype')
                value_list.append('Niet bekend')

            if "Specialisatie" not in temp_key_list:
                dictionary['Specialisatie'] = 'Niet bekend'
                temp_key_list.append('Specialisatie')
                value_list.append('Niet bekend')

            if "E-mail" not in temp_key_list:
                dictionary["E-mail"] = "Niet bekend"
                temp_key_list.append('E-mail')
                value_list.append('Niet bekend')

            for key in temp_key_list:
                del dictionary[key]

            for i in range(0,len(temp_key_list)):
                key = temp_key_list[i]
                value = value_list[i]

                dictionary[key] = value

    def write_to_csv(self):
        company_list = self.company_list
        print(company_list)
        with open('healthvalley2.csv', 'w') as file:
            try:
                headings = (self.company_list[0].keys())
                writer = csv.DictWriter(file, headings, dialect='excel')
                writer.writeheader()
                writer.writerows(company_list)
            except Exception as e:
                print(e)

s = Scraper()
s.spider()