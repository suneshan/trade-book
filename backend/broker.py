import uuid
from collections import defaultdict
from backend.currency_type import CurrencyType
from backend.order_type import OrderType

from order_book import OrderBook
from order_book_queue import OrderBookQueue
from trade_queue import TradeQueue
from trader import Trader

class Broker(object):
    def __init__(self):
        self.__broker_id = uuid.uuid1()
        self.trade_queue = TradeQueue()
        self.order_book = OrderBook(self.trade_queue)
        self.order_book_queue = OrderBookQueue(self.order_book)
        self.__traders = []

    def register_trader(self):
        trader_id = uuid.uuid1()
        self.__traders[trader_id] = Trader(trader_id)
        return trader_id

    def place_order(self, order):
        if order.trader_id in self.__traders:
            trader = self.__traders[order.trader_id]
            if order.order_type == OrderType.BUY and order.currency_type == CurrencyType.ETH:
                trader.zar_wallet().reserve(order.price * order.amount)
                self.order_book_queue.place_order(order)


    def cancel_order(self):
        t = 2

    
        

