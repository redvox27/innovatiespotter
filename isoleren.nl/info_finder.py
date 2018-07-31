import requests
from bs4 import BeautifulSoup
from headers import HEADERS
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self):
        self.url = 'https://www.isoleren.nl/content.php?pageID=4&proID=10'
        self.headers = HEADERS
        self.importer = CsvImporter('isoleren_nl')

    def find_info(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)

        td_list = soup.findAll('td', {'width': '300', 'valign': 'top'})
        for td in td_list:
            table = td.findChild('table')
            if table:
                new_td_list = table.findChildren('td')
                company = new_td_list[0].text.lstrip().rstrip()
                postcode_string = new_td_list[4].text.lstrip().rstrip()
                postcode = postcode_string[:7]
                print(company)
                print(postcode)
                self.importer.import_to_csv(company, postcode)
                print('\n')

finder = InfoFinder()
finder.find_info()
