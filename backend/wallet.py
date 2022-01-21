import uuid

class Wallet(object):
    def __init__(self, funds):
        self.wallet_id = uuid.uuid1()
        self.__funds = funds
        self.__reserved_funds = 0

    def balance(self):
        return self.__funds

    def deposit(self, funds):
        self.funds += funds

    def withdraw(self, funds):
        self.funds -= funds

    def reserve(self, funds):
        if self.__reserved_funds + funds <= self.__funds:
            self.__reserved_funds += funds
            return True
        return False

    def unreserve(self, funds):
        if  funds <= self.__reserved_funds:
            self.__reserved_funds -= funds
            return True
        return False

    def available_balance(self):
        return self.__funds - self.__reserved_funds



    
   
    
