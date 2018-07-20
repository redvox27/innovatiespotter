import requests
from bs4 import BeautifulSoup
from headers import HEADERS

class HrefFinder:

    def __init__(self):
        self.url = 'http://www.automotivenl.com/leden/leden-lijst'
        self.headers = HEADERS

    def alphabet_url_list(self):
        req = requests.get(self.url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)
        url_list = []

        pagination_list_tag = soup.find('ul', {'class': 'pagination pagination-xs'})
        ankor_list = pagination_list_tag.findChildren('a')
        del ankor_list[len(ankor_list) - 1]
        del ankor_list[len(ankor_list)-3]
        for ankor in ankor_list:
            href = ankor.get('href')
            url = 'http://www.automotivenl.com' + href
            url_list.append(url)
        return url_list

    def get_urls_to_scrape(self):
        alphabetic_url_list = self.alphabet_url_list()
        urls_to_scrape = []
        for url in alphabetic_url_list:
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            nav_bar = soup.find('nav', {'class': 'hidden-xs text-center'})

            if nav_bar:
                ankor_list = nav_bar.findChildren('a')
                for ankor in ankor_list:
                    text = ankor.text
                    if text == 'Einde':
                        href = ankor.get('href')
                        page_number_limit = int(href[-1:])
                        for i in range(1, page_number_limit + 1):
                            url_to_scrape = 'http://www.automotivenl.com' + href[:-1] + str(i)
                            urls_to_scrape.append(url_to_scrape)
            else:
                urls_to_scrape.append(url)
        return urls_to_scrape

    def get_href_list(self):
        print('collecting hrefs')
        url_list = self.get_urls_to_scrape()
        for url in url_list:
            print(url)
            req = requests.get(url, self.headers)
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            h2_headers = soup.findAll('h2', {'class': 'lead page-header'})
            if h2_headers:
                for header in h2_headers:
                    href = header.findChild('a').get('href')
                    url = 'http://www.automotivenl.com' + href
                    url_list.append(url)
        return url_list
