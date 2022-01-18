from pickle import FALSE
from display_book import DisplayBook
from order_type import OrderType
from order_book import OrderBook
from order_book_queue import OrderBookQueue
from market import Market
from order import Order

if __name__ == '__main__':
    market = Market()
    dsp = DisplayBook(market.get_order_book(), market.get_trades())
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


