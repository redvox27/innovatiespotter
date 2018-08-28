from omleidingsSites.hrefFinderController import HrefFinder

class Finder(HrefFinder):

    def __init__(self):
        super().__init__('https://www.hollandventure.com/voormalige-investeringen')

    def get_url_list(self):
        soup = self.get_soup()
        card_list = soup.findAll('div', {'class': 'span3 card'})
        company_set = set()

        for card in card_list:
            ankor = card.findChild('a')
            if ankor:
                url = ankor.get('href')
                company = card.findChild('h4').text
                company_set.add((company, url))
        return company_set
