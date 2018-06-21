import requests
from bs4 import BeautifulSoup

class HrefFinder:

    def __init__(self):
        self.url = 'http://www.dptech.nl/leden/leden/'
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def get_href_list(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)
        href_list = []

        ankor_list = soup.findAll('a')
        for ankor in ankor_list:
            href = ankor.get('href')
            if href[:27] == 'http://www.dptech.nl/leden/':
                href_list.append(href)
        return href_list[8:]


finder = HrefFinder()
finder.get_href_list()