import threading
from bs4 import BeautifulSoup
import requests
import queue

class HrefFinder(threading.Thread):

    queue = queue.Queue()

    def __init__(self):
        threading.Thread.__init__(self)
        self.url = "https://bedrijven.xyz/overzicht/"
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }


    def get_page_limit(self):
        href = ''
        soup = self.get_soup()
        ankor_list = (soup.findAll('a'))
        for ankor in ankor_list:
            if ankor.text == "Last":
                href = (ankor.get('href'))
        temp_list = href.split('/')
        limit = temp_list[len(temp_list)-1]
        return int(limit)

    def fill_url_list(self):
        limit = self.get_page_limit()
        url_list = []
        for i in range(1, limit+1):
            url = self.url + str(i)
            url_list.append(url)
        return url_list

    def get_soup(self, url="https://bedrijven.xyz/overzicht/"):
        req = requests.get(url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)
        return soup

    def run(self):
        url_list = self.fill_url_list()

        for url in url_list[:1]:
            soup = self.get_soup(url)
            item_list = soup.findAll('div', {'class': 'item'})
            if item_list:
                for item in item_list:
                    company_name = item.find('a').text
                    location = item.find('p').text
                    company_dict = {'company_name': company_name, 'location': location}
                    self.queue.put(company_dict)
