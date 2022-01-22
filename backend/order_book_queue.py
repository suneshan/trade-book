import queue
import threading
from threading import Thread

class OrderBookThread(Thread):
    def __init__(self, event, order_book, order_queue):
        Thread.__init__(self)
        self.stopped = event
        self.order_book = order_book
        self.order_queue = order_queue

    def run(self):
        while not self.stopped.wait(0.00001):
            while not self.order_queue.empty():
                self.order_book.process_order(self.order_queue.get())

class OrderBookQueue(object):
    def __init__(self, order_book):
        self.order_queue = queue.Queue()
        self.order_book = order_book
        self.stopFlag = threading.Event()
        self.order_book_thread = OrderBookThread(self.stopFlag, self.order_book, self.order_queue)
        self.order_book_thread .start()
        
    def place_order(self, order):
        self.order_queue.put(order)
    
    def stop_all_orders(self):
        self.stopFlag.set()

    def resume_orders(self):
        if not self.order_book_thread.is_alive():
            self.order_book_thread .start()

    def is_queue_alive(self):
        return self.order_book_thread.is_alive()
        
    def get_order_book(self):
        return self.order_book
