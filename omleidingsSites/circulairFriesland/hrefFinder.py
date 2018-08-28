from omleidingsSites.hrefFinderController import HrefFinder

class Finder(HrefFinder):

    def __init__(self):
        super().__init__('https://www.circulairfriesland.frl/organisatieenleden')

    def get_url_list(self):
        soup = self.get_soup()
        table = soup.find('table', {'class': 'table table--light'})
        ankor_list = table.findChildren('a')
        company_set = set()
        for ankor in ankor_list:
            try:
                href = ankor.get('href')
                company = ankor.text
                company_set.add((company, href))
            except Exception as e:
                print(e)
        return company_set
