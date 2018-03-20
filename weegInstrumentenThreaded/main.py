from weegInstrumentenThreaded.hrefFinder import HrefFinder
from weegInstrumentenThreaded.infoFinder import InfoFinder
from weegInstrumentenThreaded.csvWriter import Writer
import time

start = time.time()

href_finder = HrefFinder()
info_finder = InfoFinder(href_finder.href_queue)

info_finder.start()
href_finder.start()

info_finder.join()
href_finder.join()



stop = time.time()

print(stop - start)
