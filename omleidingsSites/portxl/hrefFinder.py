from omleidingsSites.hrefFinderController import HrefFinder

class Finder(HrefFinder):

    def __init__(self):
        super().__init__('https://www.tulypwind.com/')

    def get_url_list(self):
        soup = self.get_soup()
        