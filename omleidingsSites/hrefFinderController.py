import requests
from bs4 import BeautifulSoup
from headers import HEADERS

class HrefFinder:

    def __init__(self, url):
        self.url = url

    def get_soup(self):
        try:
            req = requests.get(self.url, HEADERS)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)
            return soup
        except Exception as e:
            print(e)

    def get_url_list(self):
        pass