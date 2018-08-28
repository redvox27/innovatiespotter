from omleidingsSites.hrefFinderController import HrefFinder

class Finder(HrefFinder):

    def __init__(self):
        super().__init__('https://biopartnerleiden.nl/huurders')

    def get_url_list(self):
        soup = self.get_soup()
        card_contents = soup.findAll('div', {'class': 'col-sm-6'})
        company_set = set()
        for card in card_contents:
            try:
                company = card.findChild('h4').text.lstrip().rstrip()
                url = card.findChild('a').get('href')
                if url != '':
                    print(company)
                    print(url)
                    company_set.add((company, url))
            except Exception as e:
                print(e)
        return company_set
