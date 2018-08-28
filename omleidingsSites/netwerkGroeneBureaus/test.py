import requests
from bs4 import BeautifulSoup
from headers import HEADERS

url_list = ['http://www.gimaris.com', 'http://www.aquaterranova.nl', 'http://www.altwym.nl']
for url in url_list:
    req = requests.get(url, HEADERS)
    plain_text = req.text
    print(plain_text)
    soup = BeautifulSoup(plain_text)
    ankor_list = soup.findAll('a')
    print(ankor_list)
    # for ankor in ankor_list:
    #     try:
    #         href = ankor.get('href')
    #         print(href)
    #     except Exception as e:
    #         print(ankor)
