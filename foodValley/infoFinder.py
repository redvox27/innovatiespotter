import requests
from bs4 import BeautifulSoup
import threading
from queue import Queue
from foodValley.urlList import UrlList


class InfoFinder(threading.Thread):


    dict_queue = Queue()

    def __init__(self):
        threading.Thread.__init__(self)
        self.url_list = UrlList.url_list
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def clear_address_list(self, address_column):
        delete_list = ['\t', '\n', '\xa0', '\n\t']
        address_list = address_column.split('<br/>')
        for element in address_list:
            if element == ' ':
                address_list.remove(element)
        return address_list

    def run(self):
        for url in self.url_list:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text, 'html.parser')

            company_name = soup.find('h1').text

            location = soup.find('span', {'class': 'member-city'}).text
            print(location)

            address_column = str(soup.find('div', {'class': 'large-6 columns member-adrress'}))

            cleared_list = self.clear_address_list(address_column)
            print(cleared_list)
