from fme.UrlFinder import UrlFinder
from fme.href_finder import HrefFinder
from fme.infoFinder import Infofinder
from fme.csvWriter import CsvWriter

url_finder = UrlFinder()
href_finder = HrefFinder(url_finder.url_queue)
info_finder = Infofinder(href_finder.href_queue)
writer = CsvWriter(info_finder.company_dict_queue)

url_finder.start()
href_finder.start()
info_finder.start()
writer.start()
