import requests
from bs4 import BeautifulSoup

class HrefFinder:

    def __init__(self):
        self.url = 'https://www.tfhc.nl/partners/'
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def fill_href_listP(self, soup):
        ankor_list = soup.findAll('a')
        href_list = []

        for ankor in ankor_list:
            href = ankor.get('href')
            if href:
                if '/partner/' in href:
                    href_list.append(href)
        return sorted(list(set(href_list)))

    def get_href_list(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)

        href_list = self.fill_href_listP(soup)

        return href_list
