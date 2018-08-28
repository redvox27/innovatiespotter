import re
import requests
from headers import HEADERS
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self):
        self.url = 'https://www.skbnl.nl/deelnemers/ledenlijst/'
        self.importer = CsvImporter('skbnl')

    def find_info(self):
        req = requests.get(self.url, HEADERS)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)
        contentList = (soup.findAll('div', {'class': 'lidContent'}))

        for content in contentList:
            match = re.search('\d{8}', str(content))
            if match:
                kvk = match.group()
                print(kvk)
                self.importer.import_kvk_to_csv(kvk)


finder = InfoFinder()
finder.find_info()