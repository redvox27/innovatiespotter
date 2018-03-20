import threading
import time
from queue import Queue

import requests
from bs4 import BeautifulSoup

class Infofinder(threading.Thread):

    company_dict_queue = Queue()
    finding = True

    def __init__(self, href_queue):
        threading.Thread.__init__(self)
        print('infofinder thread started')
        self.href_queue = href_queue
        self.headers = self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def run(self):
        time.sleep(5)
        print('method stopped sleeping')
        while not self.href_queue.empty():
            company_dict = {}
            url = self.href_queue.get()
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            company_name = soup.find('h1').text
            contact_info = str(soup.find('div', {'class': 'grid-flex__item mobile-xl-6 desktop-6'}))
            contact_info_list = contact_info.split('\n')
            address = contact_info_list[3]
            postcode = contact_info_list[4]
            place = contact_info_list[5]

            address = address.replace(' ', '')
            address = address.replace('<br/>', '')
            postcode = postcode.replace(' ', '')
            postcode = postcode.replace('\xa0', '')
            place = place.replace(' ', '')
            place = place.replace('</div>', '')
            print('company name: ' + company_name)
            print('address: ' + address)
            print('postcocde: ' + postcode)
            print('place: ' + place)
            print('\n')

            company_dict['company'] = company_name
            company_dict['adres'] = address
            company_dict['postcode'] = postcode
            company_dict['plaats'] = place

            self.company_dict_queue.put(company_dict)
        self.finding = False