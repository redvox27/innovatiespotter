import csv

import requests
from bs4 import BeautifulSoup
import threading
import time

class InfoFinder(threading.Thread):

    company_dict_list = []

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.headers = self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }
        self.url_list = []
        self.url_check_list = []
        self.queue = queue
        self.running = True
    def run(self):
        time.sleep(0.5)
        while not self.queue.empty():
            href = self.queue.get()
            if href not in self.url_check_list:
                self.url_check_list.append(href)
                req = requests.get(href, self.headers)
                plain_text = req.text
                soup = BeautifulSoup(plain_text)
                company_dict = {}
                ankor = soup.find('a', {'class': 'website'})
                website = ankor.get('href')
                company_name = soup.find('h3', {'class': 'title'})

                company_dict['company'] = company_name.text
                company_dict['website'] = website
                print(company_dict)
                self.company_dict_list.append(company_dict)

                company_list = self.company_dict_list
                print(company_list)
                with open('weeginstrumenten.csv', 'w') as file:
                    try:
                        headings = (self.company_dict_list[0].keys())
                        writer = csv.DictWriter(file, headings, dialect='excel')
                        writer.writeheader()
                        writer.writerows(company_list)
                    except Exception as e:
                        print(e)