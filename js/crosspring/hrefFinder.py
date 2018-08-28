from omleidingsSites.hrefFinderController import HrefFinder
from selenium.webdriver import ActionChains
from selenium import webdriver
from bs4 import BeautifulSoup

class Finder(HrefFinder):

    def __init__(self):
        super().__init__('http://crosspring.nl/')

    def get_url_list(self):
        driver = webdriver.Chrome(executable_path='C:/Users/vince/chromedriver/chromedriver.exe')
        driver.implicitly_wait(10)
        driver.get(self.url)
        actions = ActionChains(driver)
        actions.move_by_offset(514.28125, 646)
        actions.perform()
        actions.click()
        company_set = set()
        soup = BeautifulSoup(driver.page_source)
        col = soup.find('section', {'class': 'col-5-1'})
        column_list = col.findChildren('div', {'class': 'column'})
        for column in column_list:
            ankor = column.findChild('a')
            if ankor:
                href = ankor.get('href')
                if href:
                    href = href.lstrip().rstrip()
                    company = column.text.lstrip().rstrip()
                    company_set.add((company, href))
        return company_set

