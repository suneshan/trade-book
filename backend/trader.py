from currency_type import CurrencyType
from wallet import Wallet

class Trader(object):
    def __init__(self, trader_id):
        self.trader_id = trader_id
        self.eth_wallet = Wallet()
        self.zar_wallet = Wallet()