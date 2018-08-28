from omleidingsSites.infoFinderController import InfoFinder
from omleidingsSites.biopartnerLeiden.hrefFinder import Finder

hrefFinder = Finder()
company_set = hrefFinder.get_url_list()
infoFinder = InfoFinder(company_set, 'biopartnerleiden')
infoFinder.find_info()