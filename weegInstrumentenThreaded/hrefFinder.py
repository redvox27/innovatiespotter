import threading
import requests
from bs4 import BeautifulSoup
from queue import Queue

class HrefFinder(threading.Thread):

    href_queue = Queue()

    def __init__(self):
        threading.Thread.__init__(self)
        self.url = 'http://www.weeginstrumenten.nl/leden/'

        self.headers = self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def run(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)

        ankor_list = soup.findAll('a')
        for ankor in ankor_list:
            href = ankor.get('href')
            if '/author' in href:
                self.href_queue.put(href)
                print(href)