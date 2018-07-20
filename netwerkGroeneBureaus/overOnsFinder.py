import requests
from bs4 import BeautifulSoup
from netwerkGroeneBureaus.urlFinder import UrlFinder
from headers import HEADERS

class OverOnsFinder:

    def __init__(self):
        self.finder = UrlFinder()
        self.headers = HEADERS

    def is_complete_url(self, href):
        check_list = ['/contact', 'www']
        count = 0

        for element in check_list:
            if element in href:
                count += 1

        if count == 2:
            return True
        else:
            return False

    def get_over_ons_url_list(self):
        netwerk_url_list = self.finder.get_url_list()
        over_ons_url_set = set()
        no_contact_set = set()

        for tuple in netwerk_url_list:
            netwerk_url = tuple[1]
            company = tuple[0]
            print(netwerk_url)
            req = requests.get(netwerk_url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)
            ankor_list = soup.findAll('a')

            for ankor in ankor_list:
                href = ankor.get('href')
                if href:
                    if self.is_complete_url(href):
                        over_ons_url_set.add((company, netwerk_url, href))
                    elif '/contact' in href:
                        url = netwerk_url + href
                        over_ons_url_set.add((company, netwerk_url, url))
                    else:
                        no_contact_set.add((company, netwerk_url, href))
        return [over_ons_url_set, no_contact_set]
