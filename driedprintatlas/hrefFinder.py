import requests
from bs4 import BeautifulSoup
from headers import HEADERS
import time

class HrefFinder:

    def __init__(self):
        self.url = 'https://www.driedprintatlas.nl/list-indexed-business?search_api_views_fulltext=&field_value_chain_position=All&page='
        self.headers = HEADERS
        self.inital_url_list = []
        self.fill_initial_url_list()

    def fill_initial_url_list(self):
        for i in range(1, 71):
            url = self.url + str(i)
            self.inital_url_list.append(url)

    def get_url_list(self):
        url_list = []
        for url in self.inital_url_list:
            try:
                soup = BeautifulSoup(requests.get(url, self.headers).text)
                div_list = soup.findAll('div', {'class': 'field-title'})
                for div in div_list:
                    href = div.findChild('a').get('href')
                    url = 'https://www.driedprintatlas.nl' + href
                    url_list.append(url)
                    break
            except ConnectionError as e:
                print(e)
                time.sleep(10)
        return url_list

