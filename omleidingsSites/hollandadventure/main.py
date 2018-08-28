from omleidingsSites.infoFinderController import InfoFinder
from omleidingsSites.hollandadventure.hrefFinder import Finder
from omleidingsSites.hollandadventure.voormaligeInvesteringen import Finder as voormaligeFinder

hrefFinder = voormaligeFinder()
url_list = hrefFinder.get_url_list()
infoFinder = InfoFinder(url_list, 'hollandadventure')
infoFinder.find_info()

