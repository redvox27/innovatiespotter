import requests
from bs4 import BeautifulSoup
from headers import HEADERS

class HrefFinder:

    def __init__(self):
        self.url = 'http://www.medtechpartners.nl/home/innovaties/page/'
        self.initional_url_list = []
        self.fill_url_list()

    def fill_url_list(self):
        for i in range(1, 4):
            page_number = str(i)
            url = self.url + page_number
            self.initional_url_list.append(url)

    def get_url_list(self):
        url_list = []
        for url in self.initional_url_list:
            req = requests.get(url, HEADERS)
            html = req.text
            soup = BeautifulSoup(html)
            company_list = soup.findAll('div', {'class': 'portfolio-thumbnail-context'})
            for company in company_list:
                ankor = company.findChild('a')
                href = ankor.get('href')
                url_list.append(href)
            break
        return url_list
