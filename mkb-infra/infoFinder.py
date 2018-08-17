import requests
import re
from bs4 import BeautifulSoup
from headers import HEADERS
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self):
        self.url = 'https://www.mkb-infra.nl/vind-een-lid'

    def find_info(self):
        req = requests.get(self.url, HEADERS)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)

        member_result = soup.find('div', {'class': 'membersearchresult-wrapper'})
        print(member_result)

finder = InfoFinder()
finder.find_info()