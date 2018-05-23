import time
from bedrijvenXYZ.hrefFinder import HrefFinder
from bedrijvenXYZ.dataConverter import DataConverter
from bedrijvenXYZ.mysql import Mysql

href_finder = HrefFinder()
data_converter = DataConverter(href_finder.queue, href_finder.booleanObject)
mysql = Mysql(data_converter.company_list_queue, data_converter.converter_boolean)

href_finder.start()
data_converter.start()
mysql.start()