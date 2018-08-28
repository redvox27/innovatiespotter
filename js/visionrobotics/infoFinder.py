from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests

class InfoFinder:

    def __init__(self):
        self.url = 'https://www.vision-robotics.nl/plattegrond'

    def find_info(self):
        try:
            driver = webdriver.Chrome(executable_path='C:/Users/vince/chromedriver/chromedriver.exe')
            driver.get(self.url)
            driver.implicitly_wait(5)
            # actions = ActionChains(driver)
            # actions.move_by_offset(272.34375, 0.5)
            # actions.perform()
            # actions.click()
            print(driver.page_source)


        except Exception as e:
            print(e)

finder = InfoFinder()
finder.find_info()