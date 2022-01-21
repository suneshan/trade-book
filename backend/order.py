import uuid
import utils

class Order(object):
    def __init__(self, trader_id, order_type, price, amount, currency_type):
        self.trader_id = trader_id
        self.order_type = order_type   # side
        self.price = price
        self.amount = amount # size
        self.timestamp = utils.get_timestamp()
        self.order_id = uuid.uuid1()
        self.sell_currency_type = currency_type

    def __repr__(self):
        return '{0} {1} units at {2}'.format(self.order_type, self.amount, self.price)