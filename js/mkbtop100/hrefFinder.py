import requests
from bs4 import BeautifulSoup
from headers import HEADERS
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

class HrefFinder:

    def __init__(self):
        self.url = 'https://www.mkbinnovatietop100.nl/site/top-100-2008'
        self.headers = HEADERS

    def get_url_list(self):
        driver = webdriver.Chrome(executable_path='C:/Users/Gebruiker/chromedriver/chromedriver.exe')
        driver.implicitly_wait(10)
        driver.get(self.url)
        zuid_holland_button = driver.find_element_by_css_selector("a[index='12']")
        actions = ActionChains(driver)
        actions.move_to_element(zuid_holland_button)
        actions.perform()
        actions.click()
        url_list = []

        soup = BeautifulSoup(driver.page_source)
        company_list = soup.find('div', {'id': 'list'})
        summary_list = company_list.findChildren('div', {'class': 'summary'})
        for summary in summary_list:
            try:
                href = summary.find('a').get('href')
                url = 'https://www.mkbinnovatietop100.nl' + href
                url_list.append(url)
            except:
                pass

        return url_list
