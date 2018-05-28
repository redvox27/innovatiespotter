import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import threading
from queue import Queue

class HrefFinder():
    tutorial = 'https://medium.freecodecamp.org/better-web-scraping-in-python-with-selenium-beautiful-soup-and-pandas-d6390592e251'

    def __init__(self):

        self.url = 'http://www.hightechnl.nl/vereniging/ledenlijst'
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }
        self.url_list = set()
        self.fill_url_list()

    def fill_url_list(self):
        driver = webdriver.Chrome(executable_path='C:/Users/vincent/chromedriver/chromedriver.exe')
        driver.implicitly_wait(30)
        driver.get(self.url)

        python_button = driver.find_element_by_css_selector('label[for=listButton]')
        python_button.click()

        soup = BeautifulSoup(driver.page_source)

        ankor_list = (soup.findAll('a'))

        for ankor in ankor_list:
            href = ankor.get('href')
            url = 'http://www.hightechnl.nl'
            if '/vereniging' in href and 'Member' in href:
                url += href
                self.url_list.add(url)

    def get_url_list(self):
        return self.url_list

