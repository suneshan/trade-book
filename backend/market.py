import threading
from threading import Thread
import random
from order_book import OrderBook
from order import Order
from order_type import OrderType
from order_book_queue import OrderBookQueue
from trade_queue import TradeQueue

class MarketPriceThread(Thread):
    def __init__(self, event, market_price):
        Thread.__init__(self)
        self.stopped = event
        self.market_price = market_price

    def run(self):
        while not self.stopped.wait(5):
            self.market_price.set()

class MarketSellerThread(Thread):
    def __init__(self, event, market_price, order_book_queue):
        Thread.__init__(self)
        self.stopped = event
        self.market_price = market_price
        self.order_book_queue = order_book_queue

    def run(self):
        while not self.stopped.wait(0.9):
            self.order_book_queue.place_order(Order(OrderType.SELL, self.market_price.get() + random.randrange(1, 100), random.randrange(1, 100)))

class MarketBuyerThread(Thread):
    def __init__(self, event, market_price, order_book_queue):
        Thread.__init__(self)
        self.stopped = event
        self.market_price = market_price
        self.order_book_queue = order_book_queue

    def run(self):
        while not self.stopped.wait(0.9):
            self.order_book_queue.place_order(Order(OrderType.BUY, self.market_price.get() - random.randrange(1, 100), random.randrange(1, 100)))

class MarketPrice(object):
    def __init__(self):
        self.current = 50000
        self.stopFlag = threading.Event()
        self.market_price_thread = MarketPriceThread(self.stopFlag, self)
        self.market_price_thread.start()

    def set(self):
        self.current = self.current + (random.randrange(-200, +200))

    def get(self):
        return self.current

    def stop(self):
        self.stopFlag.set()

class Market(object):
    def __init__(self):
        self.trade_queue = TradeQueue()
        self.order_book = OrderBook(self.trade_queue)
        self.ob_queue = OrderBookQueue(self.order_book)
        self.market_price = MarketPrice()
        self.stopFlag = threading.Event()
        self.market_buyer_thread = MarketBuyerThread(self.stopFlag, self.market_price, self.ob_queue)
        self.market_buyer_thread.start()
        self.market_seller_thread = MarketSellerThread(self.stopFlag, self.market_price, self.ob_queue)
        self.market_seller_thread.start()

    def close_market(self):
        self.ob_queue.stop_all_orders()
        self.stopFlag.set()
        self.market_price.stop()

    def get_order_book(self):
         return self.order_book

    def get_trades(self):
        return self.trade_queue

    def get_market_price(self):
        return self.market_price.get()

