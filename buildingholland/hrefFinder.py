import requests
from bs4 import BeautifulSoup

class HrefFinder:

    def __init__(self):
        self.url = 'https://www.buildingholland.nl/partners-2018'
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def get_href_list(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)

        ankor_list = soup.findAll('a')
        url_list = []
        for ankor in ankor_list:
            href = ankor.get('href')
            if href:
                if '/partners-2018/' in href:
                    url = 'https://www.buildingholland.nl' + href
                    url_list.append(url)

        return url_list
