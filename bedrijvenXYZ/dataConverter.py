import threading
import queue
import time
from bedrijvenXYZ.converterBoolean import ConverterBoolean

class DataConverter(threading.Thread):

    company_list_queue = queue.Queue()
    converter_boolean = ConverterBoolean()

    def __init__(self, queue, boolean_object):
        threading.Thread.__init__(self)
        self.queue = queue
        self.boolean_object = boolean_object

    def retrieve_company_list_from_queue(self):
        company_dict = self.queue.get()
        if company_dict:
            values = list(company_dict.values())
            company = values[0]
            location = values[1]
            location = location.replace('\t', '')
            addres_list = location.split(',')
            postcode = addres_list[1]
            address = addres_list[0]
            company_list = [company.encode(), address.encode(), postcode.encode()]
            return company_list

    def put_list_in_queue(self, list):
        self.company_list_queue.put(list)

    def run(self):
        while self.boolean_object.get_boolean():
            company_list = self.retrieve_company_list_from_queue()
            self.put_list_in_queue(company_list)

        while not self.queue.empty():
            company_list = self.retrieve_company_list_from_queue()
            self.put_list_in_queue(company_list)

        self.converter_boolean.set_boolean()