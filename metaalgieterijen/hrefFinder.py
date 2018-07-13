import requests
from bs4 import BeautifulSoup

class HrefFinder:

    def __init__(self):
        self.url = 'http://www.metaalgieterijen.nl/MGB-leden.html'
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def get_url_list(self, soup):
        url_list = []
        ankor_list = soup.findAll('a')

        for ankor in ankor_list:
            href = ankor.get('href')
            if href:
                if '.html' in href:
                    url = 'http://www.metaalgieterijen.nl/' + href
                    if url not in url_list:
                        url_list.append(url)
        return url_list

    def get_href_list(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)
        url_list = self.get_url_list(soup)
        return url_list
