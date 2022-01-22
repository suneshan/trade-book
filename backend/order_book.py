from trade import Trade
import utils
from collections import defaultdict
from order_type import OrderType
from itertools import count

class OrderBook(object):
    def __init__(self, trade_queue):
        """ Orders stored as two defaultdicts of {price:[orders at price]}
            Orders sent to OrderBook through OrderBook.unprocessed_orders queue
        """
        self.__buyers = defaultdict(list)
        self.__sellers = defaultdict(list)
        self.trade_queue = trade_queue
        self.max_buy_orders = 10
        self.max_sell_orders = 10

    @property
    def max_bid(self):
        if self.__buyers:
            return max(self.__buyers.keys())
        else:
            return 0.

    @property
    def min_offer(self):
        if self.__sellers:
            return min(self.__sellers.keys())
        else:
            return float('inf')

    @property
    def max_buy_orders_reached(self):
        return len(self.__buyers) >= self.max_buy_orders

    @property
    def max_sell_orders_reached(self):
        return len(self.__sellers) >= self.max_sell_orders

    def process_order(self, incoming_order):
        """ Main processing function. If incoming_order matches then delegate to process_match """
        incoming_order.timestamp = utils.get_timestamp()
        if incoming_order.side == OrderType.BUY:
            if incoming_order.price >= self.min_offer and self.__sellers:
                self.__process_match(incoming_order)
            else:
                if not self.max_buy_orders_reached:
                    self.__buyers[incoming_order.price].append(incoming_order)
        else:
            if incoming_order.price <= self.max_bid and self.__buyers:
                self.__process_match(incoming_order)
            else:
                if not self.max_sell_orders_reached:
                    self.__sellers[incoming_order.price].append(incoming_order)
    
    def __process_match(self, incoming_order):
        """ Match an incoming order against orders on the other side of the book, in price-time priority """
        levels = self.__buyers if incoming_order.side == OrderType.SELL else self.__sellers
        prices = sorted(levels.keys(), reverse=(incoming_order.side == OrderType.SELL))
        def price_doesnt_match(book_price):
            if incoming_order.side == OrderType.BUY:
                return incoming_order.price < book_price
            else:
                return incoming_order.price > book_price

        for (i, price) in enumerate(prices):
            if (incoming_order.size == 0) or (price_doesnt_match(price)):
                break
            orders_at_level = levels[price]
            for (j, book_order) in enumerate(orders_at_level):
                if incoming_order.size == 0:
                    break
                trade = self.__execute_match(incoming_order, book_order)
                incoming_order.size = max(0, incoming_order.size-trade.size)
                book_order.size = max(0, book_order.size-trade.size)
                self.trade_queue.create(trade)
            levels[price] = [o for o in orders_at_level if o.size > 0]
            if len(levels[price]) == 0:
                levels.pop(price)
        # If the incoming order has not been completely matched, add the remainder to the order book
        if incoming_order.size > 0:
            same_side = self.__buyers if incoming_order.side == OrderType.BUY else self.__sellers
            same_side[incoming_order.price].append(incoming_order)

    def __execute_match(self, incoming_order, book_order):
        trade_size = min(incoming_order.size, book_order.size)
        return Trade(incoming_order.side, book_order.price, trade_size, incoming_order.order_id, book_order.order_id, utils.get_timestamp(), incoming_order.wallet_id, book_order.wallet_id)



    
if __name__ == "__main__": 
    testorders = defaultdict(list)
    order = (OrderType.SELL, 50000, 0.1)
    testorders[50000].append(order)
    order = (OrderType.SELL, 50000, 0.2)
    testorders[50000].append(order)
    order = (OrderType.SELL, 60000, 0.5)
    testorders[60000].append(order)
    print (testorders[50000])
    testorders[50000].pop(1)
    print (testorders[50000])
   