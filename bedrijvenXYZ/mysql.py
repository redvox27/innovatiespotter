import pymysql
import threading

class Mysql(threading.Thread):

    def __init__(self, queue, con_bool):
        threading.Thread.__init__(self)
        self.queue = queue
        self.converter_boolean = con_bool
        self.db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Vtl54711', db='bedrijven')
        self.cursor = self.db.cursor()

    def insert_data_into_database(self):
        company_list = self.queue.get()
        print(company_list)
        company, address, postal_code = company_list[0], company_list[1], company_list[2]

        query = 'insert into companies (company, address, postal_code)\
                  values(%s, %s, %s)'

        self.cursor.execute(query, (company, address, postal_code))
        self.db.commit()

    def run(self):
        while self.converter_boolean.get_boolean():
            self.insert_data_into_database()

        while not self.queue.empty():
            self.insert_data_into_database()
        print("mysql done")