import requests
from bs4 import BeautifulSoup
from selenium import webdriver

class HrefFinder:

    def __init__(self):
        self.url = 'https://www.dutchfoodsystems.nl/members-guide/'
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

    def get_href_list(self):
        driver = webdriver.Chrome(executable_path='C:/Users/vincent/chromedriver/chromedriver.exe')
        driver.implicitly_wait(30)
        driver.get(self.url)

        python_button = driver.find_element_by_css_selector('li[id=menu-item-132]')
        python_button.click()

        soup = BeautifulSoup(driver.page_source)

        print(soup.findAll('a'))

finder = HrefFinder()
finder.get_href_list()