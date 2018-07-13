import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re

class HrefFinder:

    def __init__(self):
        self.url = 'https://metaalunie.nl/Metaalunie/Branches'
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def get_ankor_list(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)

        ankor_list = soup.findAll('a')

        for ankor in ankor_list:
            if '#detailid' in str(ankor):
                ankor_text = ankor.text
                href = ankor.get('href')
                url = 'https://metaalunie.nl/Metaalunie/Branches' + href

                driver = webdriver.Chrome(executable_path='C:/Users/Gebruiker/chromedriver/chromedriver.exe')
                driver.implicitly_wait(30)
                driver.get(url)

                python_button = driver.find_element_by_link_text(ankor_text)
                python_button.click()

                info_soup = BeautifulSoup(driver.page_source)
                table_body = info_soup.find('tbody')
                table_rows = table_body.findChildren('tr')

                company = table_rows[1].findChild('h2').text
                print(company)
                adres_row = table_rows[6]
                adres_data = adres_row.findChildren('td')
                splitted_adres_data = str(adres_data[1]).split('<br/>')
                print(splitted_adres_data)
                print('\n')
finder = HrefFinder()
finder.get_ankor_list()