import utils

class Trade(object):
    def __init__(self, side, price, size, order_id, book_order_id, timestamp):
        self.side = side
        self.price = price
        self.size = size
        self.incoming_order_id = order_id
        self.book_order_id = book_order_id
        self.timestamp = timestamp

    def __repr__(self):
        return '{0}: {1} {2} units at {3}'.format(utils.format_microsecond_timestamp(self.timestamp), self.side, self.size, self.price)