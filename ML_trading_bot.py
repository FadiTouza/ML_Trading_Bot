import creds
from lumibot.brokers import Alpaca                      #Broker
from lumibot.backtesting import YahooDataBacktesting    #Backtesting
from lumibot.strategies.strategy import Strategy        #The trading bot itself
from lumibot.traders import Trader                      #Gives deployemnt capability
from datetime import datetime
from alpaca_trade_api import REST
from timedelta import Timedelta

API_KEY_ID = creds.API_KEY_ID
API_SECRET_KEY = creds.API_SECRET_KEY
BASE_URL = creds.BASE_URL

ALPACA_CREDS = {
    "API_KEY" : API_KEY_ID,
    "API_SECRET" : API_SECRET_KEY,
    "PAPER" : True
}

CASH_AT_RISK = 0.5
START_DATE = datetime(2022,1,1)
END_DATE = datetime(2022,3,28)


class TradingStrategy(Strategy):
    """Contains the core strategy for the training bo t"""

    def initialize(self, symbol:str="SPY", cash_at_risk:float=CASH_AT_RISK):
        self.symbol = symbol
        self.sleeptime = "24H"
        self.cash_at_risk = cash_at_risk
        self.last_trade = None
        self.api = REST(key_id=API_KEY_ID, secret_key=API_SECRET_KEY, base_url=BASE_URL)
    

    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round((cash * self.cash_at_risk) / last_price)
        return cash, last_price, quantity


    def get_day_interval(self, amount_of_days_prior):
        today = self.get_datetime()
        days_prior = today - Timedelta(days=amount_of_days_prior)
        return days_prior.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")


    def get_news(self):
        days_prior, today = self.get_day_interval(3)
        news = self.api.get_news(self.symbol, start=days_prior, end=today)

        headlines = [ev.__dict__["_raw"]["headline"] for ev in news]
        summaries = [ev.__dict__["_raw"]["summary"] for ev in news]

        return headlines, summaries


    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()

        ### Check if fractional trading is supported
        if self.last_trade == None:
            headlines, summaries = self.get_news()
            print(headlines)
            print("\n\n\n")
            print(summaries)

            order = self.create_order(self.symbol, quantity, "buy", type="bracket",
                                      take_profit_price = last_price * 1.15, stop_loss_price = last_price * 0.90)
            self.submit_order(order)
            self.last_trade = "buy"





broker = Alpaca(ALPACA_CREDS)
strategy = TradingStrategy(name="RocketTrader", broker=broker,
                           parameters={"symbol":"SPY", "cash_at_risk":CASH_AT_RISK})
strategy.backtest(YahooDataBacktesting, START_DATE, END_DATE,
                  parameters={"symbol":"SPY", "cash_at_risk":CASH_AT_RISK})



