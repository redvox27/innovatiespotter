import requests
import re
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from headers import HEADERS
from csvImporter import CsvImporter

class InfoFinder:

    def __init__(self):
        self.url = 'https://www.maritiemland.nl'
        self.importer = CsvImporter('maritiemland')
        self.headers = HEADERS

    def find_info(self):
        driver = webdriver.Firefox(executable_path='C:/Users/Gebruiker/firefoxdriver/geckodriver.exe')
        driver.implicitly_wait(10)
        driver.switch_to.default_content()
        driver.get(self.url)

        action = ActionChains(driver)
        action.move_by_offset(723, 137)
        action.click()
        action.perform()

        soup = BeautifulSoup(driver.page_source)
        li_list = soup.findAll('li', {'class': 'column richtext'})
        for li in li_list:
            company_string = li.findChild('h3').text
            splitted_company_string = company_string.split('-')
            if len(splitted_company_string) > 2:
                company = splitted_company_string[0] + '-' + splitted_company_string[1].lstrip().rstrip()
            else:
                company = splitted_company_string[0].lstrip().rstrip()

            match = re.search('\d{4}\s[A-Z]{2}', str(li))
            if match:
                postcode = match.group()
                print(company)
                print(postcode)
                self.importer.import_to_csv(company, postcode)


finder = InfoFinder()
finder.find_info()
