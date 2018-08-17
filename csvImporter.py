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

    def import_coordinates_to_csv(self, company, lat, lon):
        company_dict = {}
        company_dict['company'] = company
        company_dict['lat'] = lat
        company_dict['lon'] = lon

        with open(self.filename, 'a') as file:
            try:
                headings = company_dict.keys()
                writer = csv.DictWriter(file, headings)
                writer.writerow(company_dict)
            except Exception as e:
                print(e)

    def import_kvk_to_csv(self, kvk):
        company_dict = {}
        company_dict['kvk'] = kvk

        with open(self.filename, 'a') as file:
            try:
                headings = company_dict.keys()
                writer = csv.DictWriter(file, headings)
                writer.writerow(company_dict)
            except Exception as e:
                print(e)