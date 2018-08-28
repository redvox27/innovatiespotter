from omleidingsSites.infoFinderController import InfoFinder
from omleidingsSites.circulairFriesland.hrefFinder import Finder

hrefFinder = Finder()
company_set = hrefFinder.get_url_list()
infoFinder = InfoFinder(company_set, 'circulairFriesland')
infoFinder.find_info()