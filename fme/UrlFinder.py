import threading
from queue import Queue


class UrlFinder(threading.Thread):

    url_queue = Queue()

    def __init__(self):
        threading.Thread.__init__(self)

        self.url = 'https://www.fme.nl/nl/leden/overzicht?page='
        self.headers = self.headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        }

        self.iteration_range = 158
        self.test_range = 1

    def run(self):
        for i in range(0, self.iteration_range):
            url = self.url + str(i)
            self.url_queue.put(url)