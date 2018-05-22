import threading
import queue

class DataConverter(threading.Thread):

    def __init__(self, queue, boolean_object):
        threading.Thread.__init__(self)
        self.queue = queue
        self.boolean_object = boolean_object

    def run(self):
        pass
