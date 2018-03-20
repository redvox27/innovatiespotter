import csv

class Writer():

    def __init__(self, company_dict_list):
        self.company_dict_list = company_dict_list

    def write_to_csv(self):
        company_list = self.company_dict_list
        print(company_list)
        with open('weeginstrumenten.csv', 'w') as file:
            try:
                headings = (self.company_dict_list[0].keys())
                writer = csv.DictWriter(file, headings, dialect='excel')
                writer.writeheader()
                writer.writerows(company_list)
            except Exception as e:
                print(e)
