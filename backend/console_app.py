from display_book import DisplayBook
from market import Market
from utils import Singleton

class TestSingle(object, metaclass=Singleton):
    def __init__(self):
        print('Constructor______')
        self.amount = 0

    def set_amount(self, amt):
        self.amount = amt

    def get_amount(self):
        return self.amount

if __name__ == '__main__':

    instance1 = TestSingle()
    instance1.set_amount(1000)
    print(instance1.get_amount())

    instance2 = TestSingle()
    instance2.set_amount(2000)
    print(instance1.get_amount())

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


