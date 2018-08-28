from omleidingsSites.hrefFinderController import HrefFinder

class GroeneBureauHrefFinder(HrefFinder):

    def __init__(self):
        super().__init__('https://www.netwerkgroenebureaus.nl/brancheorganisatie/ledenlijst')

    def get_url_list(self):
        try:
            soup = self.get_soup()
            url_list = []
            table = soup.find('table', {'cellspacing': '0', 'cellpadding': '0', 'border': '0'})
            ankor_list = table.findChildren('a')
            for ankor in ankor_list:
                if ankor:
                    url = ankor.get('href')
                    company = ankor.text
                    if url:
                        if url[len(url)-1] == '/':
                            url = url[:-1]
                        url_list.append((company, url))
            return url_list
        except Exception as e:
            print(e)
