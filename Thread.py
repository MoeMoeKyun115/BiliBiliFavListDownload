import threading
import time

class Worker(threading.Thread):
    def __init__(self, queue, num, lock, down_album):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = num
        self.lock = lock
        self.down_album = down_album

    def run(self):
        while self.queue.qsize() > 0:
            aid = self.queue.get()
            # self.lock.acquire()
            time.sleep(1)
            self.down_album(aid, self.num)
            # self.lock.release()
