import requests
from bs4 import BeautifulSoup

class HrefFinder:

    def __init__(self):
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

        self.url = 'https://teqnow.nl/robotatlas?page='
        self.url_list = []
        self.fill_url_list()

    def fill_url_list(self):
        for i in range(0,1):
            string_number = str(i)
            url = self.url + string_number
            self.url_list.append(url)

    def get_href_list(self):
        href_list = []
        for url in self.url_list:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            ankor_list = soup.findAll('a')

            for ankor in ankor_list:
                href = (ankor.get('href'))
                if href:
                    if 'https://teqnow.nl/robotatlas/' in href:
                        href_list.append(href)

        final_list = list(set(href_list))
        print(len(final_list))

        return final_list
