from omleidingsSites.infoFinderController import InfoFinder
from js.crosspring.hrefFinder import Finder

href_finder = Finder()
company_set = href_finder.get_url_list()
info_finder = InfoFinder(company_set, 'crosspring')
info_finder.find_info()
