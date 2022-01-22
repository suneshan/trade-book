import queue

class TradeQueue(object):
    def __init__(self, **kwargs):
           self.trade_queue = queue.Queue()

    def create(self, trade):
        self.trade_queue.put(trade)

    def get_queue(self):
        return self.trade_queue
        