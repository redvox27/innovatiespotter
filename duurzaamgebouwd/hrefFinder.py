import requests
from bs4 import BeautifulSoup
from selenium import webdriver

class HrefFinder:

    def __init__(self):
        self.url = 'https://www.duurzaamgebouwd.nl/community/filter/partners/pagina/'
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }
        self.url_list = []
        self.fill_url_list()

    def fill_url_list(self):
        for i in range(1, 12):
            url = self.url + str(i)
            self.url_list.append(url)

    def fill_href_list(self, soup, href_list):
        ankor_list = soup.findAll('a')
        for ankor in ankor_list:
            href = ankor.get('href')
            if href:
                if '/partners/c/' in href:
                    url = 'https://www.duurzaamgebouwd.nl' + href
                    href_list.append(url)

    def get_href_list(self):
        href_list = []
        for url in self.url_list:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            self.fill_href_list(soup, href_list)
        return sorted(list(set(href_list)))
