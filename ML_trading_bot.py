import creds
from lumibot.brokers import Alpaca                      #Broker
from lumibot.backtesting import YahooDataBacktesting    #Backtesting
from lumibot.strategies.strategy import Strategy        #The trading bot itself
from lumibot.traders import Trader                      #Gives deployemnt capability
from datetime import datetime

API_KEY = creds.API_KEY
API_SECRET = creds.API_SECRET
BASE_URL = creds.BASE_URL

ALPACA_CREDS = {
    "API_KEY" : API_KEY,
    "API_SECRET" : API_SECRET,
    "PAPER" : True
}

class TradingStrategy(Strategy):
    """Contains the core strategy for the training but"""

    def initialize(self, symbol:str = "SPY"):
        """Runs once when bot starts trading"""
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None

broker = Alpaca(ALPACA_CREDS)
