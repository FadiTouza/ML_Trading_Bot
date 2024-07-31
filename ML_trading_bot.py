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
    """Contains the core strategy for the training bo t"""

    def initialize(self, symbol:str = "SPY"):
        """Runs once when bot starts trading"""
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
    
    def on_trading_iteration(self):
        if self.last_trade == None:
            order = self.create_order(self.symbol, 7, "buy", type="market")
            self.submit_order(order)
            self.last_trade = "buy"

start_date = datetime(2022,1,1)
end_date = datetime(2023,12,30)

broker = Alpaca(ALPACA_CREDS)
strategy = TradingStrategy(name="RocketTrader", broker=broker,
                           parameters={"symbol":"SPY"})
strategy.backtest(YahooDataBacktesting, start_date, end_date,
                  parameters={"symbol":"SPY"})
