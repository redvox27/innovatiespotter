import requests
import re
from bs4 import BeautifulSoup
from headers import HEADERS
from csvImporter import CsvImporter
from omleidingsSites.netwerkGroeneBureaus.groeneBureausHrefFinder import GroeneBureauHrefFinder
from omleidingsSites.infoFinderController import InfoFinder

href_finder = GroeneBureauHrefFinder()
url_list = href_finder.get_url_list()
info_finder = InfoFinder(url_list, 'netwerkgroenebureaus')
info_finder.find_info()
