import csv
from hightechNL.infoFinder import InfoFinder

class CsvWriter:

    def __init__(self):
        self.info_finder = InfoFinder()

    def write_to_csv(self):
        dict_list = self.info_finder.get_dict_list()

        for company_dict in dict_list:
            print('csvWriter: ', company_dict)
            with open('hightechNL.csv', 'a') as file:
                try:
                    headings = company_dict.keys()
                    writer = csv.DictWriter(file, headings)
                    writer.writerow(company_dict)
                except Exception as e:
                    print(e)