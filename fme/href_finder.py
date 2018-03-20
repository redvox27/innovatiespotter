import threading
from queue import Queue

import requests
from bs4 import BeautifulSoup
import time

class HrefFinder(threading.Thread):

    href_queue = Queue()

    def __init__(self, url_queue):
        threading.Thread.__init__(self)
        self.url_queue = url_queue
        self.href_list = []

    def run(self):
        time.sleep(0.5)
        #todo add nv

        while not self.url_queue.empty():
            url = self.url_queue.get()
            req = requests.get(url)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            ankor_list = (soup.findAll('a'))
            for ankor in ankor_list:
                href = ankor.get('href')
                if href:
                    if '-bv' in href or '-nv' in href:
                        href = 'https://www.fme.nl' + href
                        print(href)
                        self.href_queue.put(href)

            print('\n')