import requests
import re
from bs4 import BeautifulSoup
from headers import HEADERS
from medtech.hrefFinder import HrefFinder
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self):
        self.finder = HrefFinder()
        self.url_list = self.finder.get_url_list()
        self.importer = CsvImporter('medtech')

    def find_info(self):
        for url in self.url_list:
            req = requests.get(url, HEADERS)
            html = req.text
            soup = BeautifulSoup(html)

            try:
                company = soup.find('h1', {'class': 'single-thumbnail-title post-title-color gdl-title'}).text
                single_content = soup.find('div', {'class': 'single-content'})
                paragraphs = single_content.findChildren('p')
                text = paragraphs[1].text
                self.importer.import_to_csv(company, text)
            except Exception as e:
                print(e)

finder = InfoFinder()
finder.find_info()