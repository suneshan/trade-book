from order_type import OrderType

class DisplaySummary(object):
    def __init__(self):
        self.sell_price = 0
        self.sell_amount = 0
        self.buy_price = 0
        self.buy_amount = 0

class DisplayBook(object):
    def __init__(self, order_book):
        self.order_book = order_book

    def show_order_book(self):
        # self.show_seller_orders()
        # self.show_buyer_orders()
        print('######################################################################')
        print('#      Buy Orders:                ##       Sell Orders:              #')
        print('# Price            Amount         ## Price            Amount         #')
        print('######################################################################')
        orders = {**self.order_book.sellers, **self.order_book.buyers}
        self.__display_orders(orders)
        print('######################################################################')

    def __display_orders(self, orders):
        order_summary = {}
        index = 0
        buy_found = False
        for p in sorted(orders.keys()):
            if buy_found:
                index += 1
            else:
                index -= 1
            for o in orders[p]:
                if (o.side == OrderType.BUY):
                    buy_found = True
                    if index in order_summary:
                        display_summary = order_summary.get(index)
                        if display_summary.buy_price == o.price:
                            display_summary.buy_amount += o.size
                        else:
                            display_summary.buy_price = o.price
                            display_summary.buy_amount = o.size  
                        order_summary[index] = display_summary
                    else:
                        display_summary = DisplaySummary()
                        display_summary.buy_price = o.price
                        display_summary.buy_amount = o.size 
                        order_summary[index] = display_summary
                else:
                    buy_found = False
                    if index in order_summary:
                        display_summary = order_summary.get(index)
                        if display_summary.sell_price == o.price:
                            display_summary.sell_amount += o.size
                        else:
                            display_summary.sell_price = o.price
                            display_summary.sell_amount = o.size  
                        order_summary[index] = display_summary
                    else:
                        display_summary = DisplaySummary()
                        display_summary.sell_price = o.price
                        display_summary.sell_amount = o.size 
                        order_summary[index] = display_summary
        if len(order_summary) == 0:
            print('No Orders')
        else:
            for p in reversed(order_summary):
                display_summary = order_summary[p]
                print('# {zero:6} {one:14}           ## {two:6} {three:15}          #'.format(zero = "" if display_summary.buy_price==0 else display_summary.buy_price, 
                    one = "" if display_summary.buy_amount==0 else display_summary.buy_amount, 
                    two = "" if display_summary.sell_price==0 else display_summary.sell_price, 
                    three = "" if display_summary.sell_amount==0 else display_summary.sell_amount))

    def show_trades(self):
        print(self.order_book.trades.qsize())
        print(list(self.order_book.trades.queue))
        print(self.order_book.trades.queue[1])
 