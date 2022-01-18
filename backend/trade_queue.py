class TradeQueue(object):
    def __init__(self, **kwargs):
        self.order_queue = queue.Queue()