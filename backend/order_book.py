from trade import Trade
import queue
import utils
from collections import defaultdict
from order_type import OrderType

class OrderBook(object):
    def __init__(self, trade_queue):
        """ Orders stored as two defaultdicts of {price:[orders at price]}
            Orders sent to OrderBook through OrderBook.unprocessed_orders queue
        """
        self.buyers = defaultdict(list)
        self.sellers = defaultdict(list)
        # self.unprocessed_orders = queue.Queue()
        self.trade_queue = trade_queue
        self.order_id = 0
        self.max_buy_orders = 10
        self.max_sell_orders = 10

    def new_order_id(self):
        self.order_id += 1
        return self.order_id

    @property
    def max_bid(self):
        if self.buyers:
            return max(self.buyers.keys())
        else:
            return 0.

    @property
    def min_offer(self):
        if self.sellers:
            return min(self.sellers.keys())
        else:
            return float('inf')

    @property
    def max_buy_orders_reached(self):
        return len(self.buyers) >= self.max_buy_orders

    @property
    def max_sell_orders_reached(self):
        return len(self.sellers) >= self.max_sell_orders

    def process_order(self, incoming_order):
        """ Main processing function. If incoming_order matches then delegate to process_match """
        incoming_order.timestamp = utils.get_timestamp()
        incoming_order.order_id = self.new_order_id()
        if incoming_order.side == OrderType.BUY:
            if incoming_order.price >= self.min_offer and self.sellers:
                self.process_match(incoming_order)
            else:
                if not self.max_buy_orders_reached:
                    self.buyers[incoming_order.price].append(incoming_order)
        else:
            if incoming_order.price <= self.max_bid and self.buyers:
                self.process_match(incoming_order)
            else:
                if not self.max_sell_orders_reached:
                    self.sellers[incoming_order.price].append(incoming_order)
    
    def process_match(self, incoming_order):
        """ Match an incoming order against orders on the other side of the book, in price-time priority """
        levels = self.buyers if incoming_order.side == OrderType.SELL else self.sellers
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
                trade = self.execute_match(incoming_order, book_order)
                incoming_order.size = max(0, incoming_order.size-trade.size)
                book_order.size = max(0, book_order.size-trade.size)
                self.trades.put(trade)
            levels[price] = [o for o in orders_at_level if o.size > 0]
            if len(levels[price]) == 0:
                levels.pop(price)
        # If the incoming order has not been completely matched, add the remainder to the order book
        if incoming_order.size > 0:
            same_side = self.buyers if incoming_order.side == OrderType.BUY else self.sellers
            same_side[incoming_order.price].append(incoming_order)

    def execute_match(self, incoming_order, book_order):
        trade_size = min(incoming_order.size, book_order.size)
        return Trade(incoming_order.side, book_order.price, trade_size, incoming_order.order_id, book_order.order_id, utils.get_timestamp())



    
