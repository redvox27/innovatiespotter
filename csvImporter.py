import csv

class CsvImporter:

    def __init__(self, filename):
        self.filename = filename + '.csv'

    def import_to_csv(self, company, postcode):
        company_dict = {}
        company_dict['company'] = company
        company_dict['postcode'] = postcode

        with open(self.filename, 'a') as file:
            try:
                headings = company_dict.keys()
                writer = csv.DictWriter(file, headings)
                writer.writerow(company_dict)
            except Exception as e:
                print(e)
