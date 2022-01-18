from pickle import FALSE
from display_book import DisplayBook
from order_type import OrderType
from order_book import OrderBook
from order_book_queue import OrderBookQueue
from market import Market
from order import Order

if __name__ == '__main__':
    market = Market()
    # ob_queue = OrderBookQueue()
    dsp = DisplayBook(market.get_order_book())
    # orders = [Order(OrderType.BUY, 1., 10),
    #         Order(OrderType.BUY, 1., 10),
    #         Order(OrderType.BUY, 5., 10),
    #         Order(OrderType.SELL, 12., 5),
    #         Order(OrderType.SELL, 15., 10),
    #         Order(OrderType.BUY, 11., 10),
    #         Order(OrderType.SELL, 20., 10),
    #         Order(OrderType.SELL, 30., 10),
    #         Order(OrderType.SELL, 40., 10),
    #         Order(OrderType.SELL, 50., 10),
    #         Order(OrderType.SELL, 60., 10),
    #         Order(OrderType.SELL, 70., 10),
    #         Order(OrderType.SELL, 80., 10),
    #         Order(OrderType.SELL, 100., 10),
    #         Order(OrderType.SELL, 90., 10)]
    # for order in orders:
    #     ob_queue.place_order(order)
    # ob_queue.place_order(Order(OrderType.SELL, 5., 2))
    # ob_queue.place_order(Order(OrderType.BUY, 15., 2))

    exit=False
    while not exit:
        print ('''
            1. Display Order Book
            2. Display Trades
            3. Display Market Price
            9. Exit
        ''')
        ans=input("What would you like to do?")
        if ans=="1": 
            dsp.show_order_book()
        elif ans=="2":
            dsp.show_trades()
        elif ans=="3":
            print('Market Price {0}'.format(market.get_market_price()))
        elif ans=="9":
            market.close_market()
            exit=True

    # list(collections.deque((1, 2, 3)))


