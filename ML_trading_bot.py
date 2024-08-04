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

    def initialize(self, symbol:str="SPY", cash_at_risk:float=0.5):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.cash_at_risk = cash_at_risk
        self.last_trade = None
    
    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round((cash * self.cash_at_risk) / last_price)
        return cash, last_price, quantity

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()

        ### Check if fractional trading is supported
        if self.last_trade == None:
            order = self.create_order(self.symbol, quantity, "buy", type="bracket",
                                      take_profit_price = last_price * 1.15, stop_loss_price = last_price * 0.90)
            self.submit_order(order)
            self.last_trade = "buy"




start_date = datetime(2022,1,1)
end_date = datetime(2022,3,28)

broker = Alpaca(ALPACA_CREDS)
strategy = TradingStrategy(name="RocketTrader", broker=broker,
                           parameters={"symbol":"SPY", "cash_at_risk":0.5})
strategy.backtest(YahooDataBacktesting, start_date, end_date,
                  parameters={"symbol":"SPY", "cash_at_risk":0.5})
