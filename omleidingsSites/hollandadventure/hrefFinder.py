from omleidingsSites.hrefFinderController import HrefFinder

class Finder(HrefFinder):

    def __init__(self):
        super().__init__('https://www.hollandventure.com/huidige-investeringen.html')

    def get_url_list(self):
        soup = self.get_soup()
        web_container = soup.findChild('div', {'class': 'webcontainer gridcontainer'})
        cards = web_container.findChildren('div', {'class': 'span3 card'})
        company_set = set()
        for card in cards:
            company = card.findChild('h4').text
            href = card.findChild('a').get('href')
            company_set.add((company, href))
        return company_set
