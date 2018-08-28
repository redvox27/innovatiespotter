import requests
from bs4 import BeautifulSoup
from headers import HEADERS
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

class HrefFinder:

    def __init__(self):
        self.url = 'https://www.creditexpo.nl/exposantenlijst/'

    def get_url_list(self):
        driver = webdriver.Chrome(executable_path='C:/Users/Gebruiker/chromedriver/chromedriver.exe')
        driver.implicitly_wait(10)
        driver.get(self.url)
        button = driver.find_element_by_css_selector("path[d='M0 16h28v4H0zM0 24h28v4H0zM0 8h28v4H0zM0 0h28v4H0z']")
        actions = ActionChains(driver)
        actions.move_to_element(button)
        actions.perform()
        actions.click()
        url_list = []
        soup = BeautifulSoup(driver.page_source)
        ankor_list = soup.findAll('a')

        for ankor in ankor_list:
            if ankor:
                href = ankor.get('href')
                if href:
                    if 'dienstverlener' in href:
                        url_list.append(href)
        return url_list
