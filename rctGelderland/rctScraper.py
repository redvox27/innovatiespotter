from bs4 import BeautifulSoup
import requests
import json
import csv

class RctScraper:

    def __init__(self):
        self.url = 'https://rctgelderland.nl/companies-'
        self.url_list =[]
        self.fill_url_list()
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }
        self.company_list = self.fill_company_url_list()
        self.dict_list = []

    def fill_url_list(self):
        for i in range(1, 10):
            url = self.url + str(i) + '.json'
            self.url_list.append(url)

    def fill_company_url_list(self):
        company_list = []
        for url in self.url_list:
            req = requests.get(url, self.headers)
            plain_text = req.text

            json_array = json.loads(plain_text)

            for dictionary in json_array:
                id = str(dictionary['id'])
                slug = dictionary['slug']
                company_url = 'https://rctgelderland.nl/netwerk/' + id + '/' + slug
                company_list.append(company_url)
        return company_list

    def spider(self):
        for url in self.company_list:
            print(url)
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)
            company_name = soup.find('h1').text
            sector = soup.find('h4').text
            regio = soup.find('span', {'class': 'region'}).text

            data_list = soup.findAll('dd')
            vestigins_data_list = str(data_list[0]).split('<br/>')

            adres = vestigins_data_list[0]
            postcode = vestigins_data_list[1]
            if len(data_list) < 3:
                data = data_list[1].text
                if 'www' in data:
                    website = data
                    tags = '-'
                else:
                    website = '-'
                    tags = data
            elif len(data_list) == 4:
                website = data_list[3].text
                tags = data_list[2].text
            else:
                website = (data_list[2].text)
                tags = data_list[1].text

            adres = adres.replace('\n', '')
            adres = adres.replace(' ', '')
            adres = adres.replace('<dd>', '')

            postcode = postcode.replace('\n', '')
            postcode = postcode.replace(' ', '')
            postcode = postcode.replace('</dd>', '')
            postcode = postcode[:6] + ' ' + postcode[6:]

            website = website.replace('\n', '')
            website = website.replace(' ', '')

            company_dict = {'Name': company_name, 'Sector': sector,
                            'Regio': regio, 'Adres': adres,
                            'Postcode': postcode, 'Website': website,
                            'Tags': tags}
            self.dict_list.append(company_dict)

        self.write_to_csv()

    def write_to_csv(self):
        company_list = self.dict_list
        print(company_list)
        with open('healthvalley2.csv', 'w') as file:
            try:
                headings = (self.dict_list[0].keys())
                writer = csv.DictWriter(file, headings, dialect='excel')
                writer.writeheader()
                writer.writerows(company_list)
            except Exception as e:
                print(e)
s = RctScraper()
s.spider()