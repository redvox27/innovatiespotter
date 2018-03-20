import csv
import threading
import time
from fme.infoFinder import Infofinder
class CsvWriter(threading.Thread):

    def __init__(self, company_dict_queue):
        threading.Thread.__init__(self)
        self.company_dict_queue = company_dict_queue

    def run(self):
        time.sleep(10)
        while Infofinder.finding:
            if not self.company_dict_queue.empty():
                company_dict = self.company_dict_queue.get()
                print(company_dict)
                with open('fme.csv', 'a') as file:
                    try:
                        headings = company_dict.keys()
                        writer = csv.DictWriter(file, headings)
                        writer.writerow(company_dict)
                        time.sleep(1)
                    except Exception as e:
                        print(e)
                        print('exception raised')
