import requests
from bs4 import BeautifulSoup
import csv
from rvo.Helper import Helper
import time
from rvo.testHelper import TestHelper

class Scraper:

    def __init__(self):
        self.helper = Helper()
        self.sector_dictionary = self.helper.get_dictionary()
        #in de url_dict zitten alle url's van de resultaten vd sectoren. Dit wordt gebruikt om de aantal pagina's per pagina te bepalen voor de sector
        self.url_dict = {}
        self.key_list = []

        #hierin komen alle href's per sector
        self.href_dict = {}
        self.project_dict_list = []
        self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

        self.fill_url_dict()
        self.iteration_range = len(self.url_dict)
        #self.iteration_range = 3
    '''
    fill_url_dict() vult de url_dict variabel met de urls voor de resultaten per sector
    '''
    def fill_url_dict(self):

        for key in self.sector_dictionary.keys():
            self.key_list.append(key)
            self.url_dict[key] = 'https://www.rvo.nl/subsidies-regelingen/projecten?f%5B0%5D=subsidies%' + self.sector_dictionary[key] + "&page="

    '''
    get_href_per_sector() krijgt alle href's per resultatenpagina van een sector
    en stopt vervolgens de hrefs per sector in een lijst. De lijst komt in een dictionary. 
    '''
    def get_href_per_sector(self):
        for i in range(0, self.iteration_range):
            key = self.key_list[i]
            print("key", key)
            amount_of_pages = self.determine_page_numbers(key)
            href_list = []
            print(amount_of_pages)

            #als er meer pagina's gevonden zijn voor een sector dan 1
            if amount_of_pages is not None and amount_of_pages != 0:

                for i in range(0, amount_of_pages):
                    self.fill_href_dict(key=key, index=i, href_list=href_list)
                    time.sleep(1)
            else:
                url = self.url_dict[key]
                print('no pages found, key is: ', key)
                url += str(0)
                req = requests.get(url, self.headers)
                plain_text = req.text
                soup = BeautifulSoup(plain_text)
                result_list = soup.findAll('a')

                for result in result_list:
                    href = result.get('href')
                    if "https" in href and "projecten" in href:
                        href_list.append(href)
                        self.href_dict[key] = href_list

            print('end section')
            print('\n')
    """
    fill_href_dict is een helper methode voor get_href_per_sector
    deze methode maakt een url aan de hand van de index en key dat is opgegeven in de methode van get_href_per_sector.
    de methode stopt alle hrefs per bedrijf in een lijst en maakt vervolgens een key aan in een dict met de lijst
    """
    def fill_href_dict(self, key, index, href_list):
        url = self.url_dict[key] + str(index)
        print(url)
        req = requests.get(url, self.headers)
        if req:
            plain_text = req.text
            soup = BeautifulSoup(plain_text)

            result_list = soup.findAll('a')
            for result in result_list:
                href = result.get('href')
                if "https" in href and "projecten" in href:
                    href_list.append(href)
                    self.href_dict[key] = href_list
    '''
    determine_amount_of_results() bepaald het aantal zoek resultaten per sector.
    dit is een helper methode voor determine_page_numbers. 
    '''
    def determine_amount_of_results(self, key):
        url = self.url_dict[key]
        req = requests.get(url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)

        try:
            amount_of_results = soup.find("div", attrs={"id": "result-meta"})

            if amount_of_results:

                result_text = amount_of_results.text
                result_text = result_text.replace('.', '')
                result_list = result_text.split(' ')

                return int(result_list[0])

            else:
                return None
        except Exception as e:
            print('Exception found: ' + str(e))
    '''
    determine_page_numbers bepaald het aantal pagina's voor een zoekresultaat per sector.
    voorbeeld: https://www.rvo.nl/subsidies-regelingen/projecten?f%5B0%5D=sectoren%3A5579 heeft drie pagina's aan zoek resultaten
    Dit is een helper methode voor get_href_per_sector 
    '''
    def determine_page_numbers(self, key):
        url = self.url_dict[key]
        req = requests.get(url, self.headers)
        plain_text = req.text
        soup = BeautifulSoup(plain_text)
        page_counter = 0
        result_count = self.determine_amount_of_results(key)
        pager = soup.findAll("ul", attrs={"class": "pager"})

        if result_count is None:
            return 0

        elif result_count <= 10:
            return 0

        else:

            for ankor in pager:
                last_page_href = ((soup.find('a', attrs={'title': 'Ga naar laatste pagina'})))
                href = (str(last_page_href.get('href')))

                split_href = (href.split('page='))
                page_counter = int(split_href[1])
            return page_counter + 1

    def scrape_content_view(self, soup, href):
        layout_main_column = soup.find('aside', attrs={'id': 'row1-col-asides'})
        try:
            content_view = layout_main_column.find('div', attrs={'view-content'})

            return content_view

        except Exception as e:
            print(e)
            print('href with error: ' + str(href))
            return None

    def get_rijksbijdrage(self, content_view):
        rijksbijdrage_tag = content_view.find('span', attrs={'class': 'rijksbijdrage'})
        return rijksbijdrage_tag.text

    def get_location(self, soup):
        span_list = soup.findAll('span')
        location_span = (span_list[len(span_list) - 1])
        location = location_span.text
        return location

    def content_view_to_string(self, contentview):
        contentview_string = ''
        for element in contentview:
            contentview_string += str(element)
        return  contentview_string

    def is_status_present(self, content_view_list):

        if len(content_view_list) == 17:
            return True
        else:
            return False

    def write_to_csv(self):
        company_list = self.project_dict_list
        print(company_list)
        with open('rvo.csv', 'w') as file:
            try:
                headings = (self.project_dict_list[0].keys())
                writer = csv.DictWriter(file, headings, dialect='excel')
                writer.writeheader()
                writer.writerows(company_list)
            except Exception as e:
                print(e)

    def spider(self):
        self.get_href_per_sector()
        for i in range(0, self.iteration_range):

            key = self.key_list[i]

            href_list = (self.href_dict[key])

            for j in range(0, len(href_list)):
                href = href_list[j]

                req = requests.get(href)
                plain_text = req.text
                soup = BeautifulSoup(plain_text)

                content_view = self.scrape_content_view(soup, href)
                if content_view:
                    content_view_string = self.content_view_to_string(content_view)

                    main_page_text = soup.find('div', {'class': 'content'}).text
                    #print(main_page_text)
                    print('\n')

                    rijksbijdrage = self.get_rijksbijdrage(content_view)
                    location = self.get_location(soup)
                    content_view_list = content_view_string.split('>')
                    print(rijksbijdrage)
                    project_dict = {}
                    project_dict['location'] = location
                    project_dict['rijksbijdrage'] = rijksbijdrage
                    project_dict['subsidie'] = key
                    print(len(content_view_list))
                    if self.is_status_present(content_view_list): #lenght content_view_list = 17
                        print('\033[93m' + 'status in link: ' + href)
                        print(content_view_list)
                        status_header = 'status'
                        status_data = content_view_list[7]
                        status_data = status_data.replace(' ', '')
                        status_data = status_data.replace('\n', '')
                        status_data = status_data.replace('<h4', '')
                        project_dict[status_header] = status_data
                        print('status_header: ' + status_header)
                        print('status_data: ' + status_data)

                        jaar_header = 'jaar'
                        jaar_data = content_view_list[9]
                        jaar_data = jaar_data.replace(' ', '')
                        jaar_data = jaar_data.replace('\n', '')
                        jaar_data = jaar_data.replace('<h4', '')
                        project_dict[jaar_header] = jaar_data

                        print('jaarheader: ' + jaar_header)
                        print('jaar_data: ' + jaar_data)

                        project_nummer_header = 'projectnummer'
                        project_nummer_data = content_view_list[11]
                        project_nummer_data = project_nummer_data.replace(' ', '')
                        project_nummer_data = project_nummer_data.replace('\n', '')
                        project_nummer_data = project_nummer_data.replace('<h4', '')
                        project_dict[project_nummer_header] = project_nummer_data

                        print('project_nummer_header: ' + project_nummer_header)
                        print('project_nummmer_data: ' + project_nummer_data)

                        aanvrager_header = 'aanvrager'
                        aanvrager_data = content_view_list[13]
                        aanvrager_data = aanvrager_data.replace('\t', '')
                        aanvrager_data = aanvrager_data.replace('\n', '')
                        aanvrager_data = aanvrager_data.replace('<h4', '')
                        aanvrager_data = aanvrager_data[4:-10]
                        project_dict[aanvrager_header] = aanvrager_data

                        print('aanvrager_header: ' + aanvrager_header)
                        print('aanvrager_data: ' + aanvrager_data)

                        project_partner_header = 'projectpartner'
                        project_partner_data = content_view_list[15]
                        project_partner_data = project_partner_data.replace('\t', '')
                        project_partner_data = project_partner_data.replace('\n', '')
                        project_partner_data = project_partner_data.replace('</div', '')
                        project_partner_data = project_partner_data[4:-4]
                        project_dict[project_partner_header] = project_partner_data

                        print('projectpartner_header: ' + project_partner_header)
                        print('projectpartner data: ' + project_partner_data)

                    elif len(content_view_list) == 19:
                        print('\033[91m' + 'status in link: ' + href)
                        print(content_view_list)
                        status_header = 'status'
                        status_data = content_view_list[7]
                        status_data = status_data.replace(' ', '')
                        status_data = status_data.replace('\n', '')
                        status_data = status_data.replace('<h4', '')
                        project_dict[status_header] = status_data
                        print('status_header: ' + status_header)
                        print('status_data: ' + status_data)

                        jaar_header = 'jaar'
                        jaar_data = content_view_list[9]
                        jaar_data = jaar_data.replace(' ', '')
                        jaar_data = jaar_data.replace('\n', '')
                        jaar_data = jaar_data.replace('<h4', '')
                        project_dict[jaar_header] = jaar_data

                        print('jaarheader: ' + jaar_header)
                        print('jaar_data: ' + jaar_data)

                        project_nummer_header = 'projectnummer'
                        project_nummer_data = content_view_list[13]
                        project_nummer_data = project_nummer_data.replace(' ', '')
                        project_nummer_data = project_nummer_data.replace('\n', '')
                        project_nummer_data = project_nummer_data.replace('<h4', '')
                        project_dict[project_nummer_header] = project_nummer_data

                        print('project_nummer_header: ' + project_nummer_header)
                        print('project_nummmer_data: ' + project_nummer_data)

                        aanvrager_header = 'aanvrager'
                        aanvrager_data = content_view_list[15]
                        aanvrager_data = aanvrager_data.replace('\t', '')
                        aanvrager_data = aanvrager_data.replace('\n', '')
                        aanvrager_data = aanvrager_data.replace('<h4', '')
                        aanvrager_data = aanvrager_data[4:-10]
                        project_dict[aanvrager_header] = aanvrager_data

                        print('aanvrager_header: ' + aanvrager_header)
                        print('aanvrager_data: ' + aanvrager_data)

                        project_partner_header = 'projectpartner'
                        project_partner_data = content_view_list[17]
                        project_partner_data = project_partner_data.replace('\t', '')
                        project_partner_data = project_partner_data.replace('\n', '')
                        project_partner_data = project_partner_data.replace('</div', '')
                        project_partner_data = project_partner_data[4:-4]
                        project_dict[project_partner_header] = project_partner_data

                        print('projectpartner_header: ' + project_partner_header)
                        print('projectpartner data: ' + project_partner_data)

                    else: #length content_view_list = 15
                        print('\033[94m' + href)

                        jaar_header = 'jaar'
                        jaar_data = content_view_list[7]
                        jaar_data = jaar_data.replace(' ', '')
                        jaar_data = jaar_data.replace('\n', '')
                        jaar_data = jaar_data.replace('<h4', '')
                        project_dict[jaar_header] = jaar_data
                        print('jaarheader: ' + jaar_header)
                        print('jaar_data: ' + jaar_data)

                        project_nummer_header = 'projectnummer'
                        project_nummer_data = content_view_list[9]
                        project_nummer_data = project_nummer_data.replace(' ', '')
                        project_nummer_data = project_nummer_data.replace('\n', '')
                        project_nummer_data = project_nummer_data.replace('<h4', '')
                        project_dict[project_nummer_header] = project_nummer_data
                        print('project_nummer_header: ' + project_nummer_header)
                        print('project_nummmer_data: ' + project_nummer_data)

                        aanvrager_header = 'aanvrager'
                        aanvrager_data = content_view_list[11]
                        aanvrager_data = aanvrager_data.replace('\t', '')
                        aanvrager_data = aanvrager_data.replace('\n', '')
                        aanvrager_data = aanvrager_data.replace('<h4', '')
                        aanvrager_data = aanvrager_data[4:-10]
                        project_dict[aanvrager_header] = aanvrager_data
                        print('aanvrager_header: ' + aanvrager_header)
                        print('aanvrager_data: ' + aanvrager_data)

                        project_partner_header = 'projectpartner'
                        project_partner_data = content_view_list[13]
                        project_partner_data = project_partner_data.replace('\t', '')
                        project_partner_data = project_partner_data.replace('\n', '')
                        project_partner_data = project_partner_data.replace('</div', '')
                        project_partner_data = project_partner_data[4:-4]
                        project_dict[project_partner_header] = project_partner_data

                        project_dict['status'] = '-'

                        print('projectpartner_header: ' + project_partner_header)
                        print('projectpartner data: ' + project_partner_data)
                    self.project_dict_list.append(project_dict)
                    print(project_dict)
s = Scraper()
s.spider()
s.write_to_csv()
