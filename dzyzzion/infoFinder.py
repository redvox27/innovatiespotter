import requests
from bs4 import BeautifulSoup
from headers import HEADERS
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self):
        self.url = 'https://wix-visual-data.appspot.com/app/file?compId=comp-j0xxmdmn&instance=gBPY2NaG3EPQMPq7t9NkYkIXdHzyTbw_2xFhFYxImMI.eyJpbnN0YW5jZUlkIjoiMWY4OGFjYTMtYzIwYi00OWQ4LThiYmEtYTRmNTdkMjk3YTljIiwiYXBwRGVmSWQiOiIxMzQxMzlmMy1mMmEwLTJjMmMtNjkzYy1lZDIyMTY1Y2ZkODQiLCJtZXRhU2l0ZUlkIjoiYjIwMmE5NjgtNmFjZi00YTM1LTljZDQtNDYyNjg2NjY0OTM4Iiwic2lnbkRhdGUiOiIyMDE4LTA3LTIwVDE0OjU2OjA5LjMyMloiLCJ1aWQiOm51bGwsImlwQW5kUG9ydCI6IjgyLjcyLjEwOC4xODMvNTYwMjYiLCJ2ZW5kb3JQcm9kdWN0SWQiOm51bGwsImRlbW9Nb2RlIjpmYWxzZSwiYWlkIjoiMTJjMjYwNGEtYTYwZS00YWY5LWJiN2MtODI3MDA2NjY1NTNmIiwiYmlUb2tlbiI6ImFkOGEwNWNiLWE4YzQtMDNlZC0xNzZlLWUyZDNmYjRmMzNhNCIsInNpdGVPd25lcklkIjoiY2I0MTgyM2YtN2FjYS00OGE0LTlkY2MtYTJkMzU2ZWNjMjM3In0'
        self.headers = HEADERS
        self.importer = CsvImporter('dzyzzion')

    def find_info(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        splitted_html = plain_text.split('\n')[1:]

        for company_string in splitted_html:
            splitted_string = company_string.split(',')
            company = splitted_string[2]
            adres = splitted_string[5]
            postcode = splitted_string[6] + ' ' + splitted_string[7]
            website = splitted_string[9].replace('\r', '')
            self.importer.import_to_csv(company, adres, postcode, website)
finder = InfoFinder()
finder.find_info()