import creds
from lumibot.brokers import Alpaca                      #Broker
from lumibot.backtesting import YahooDataBacktesting    #Backtesting
from lumibot.strategies.strategy import Strategy        #The trading bot itself
from lumibot.traders import Trader                      #Gives deployemnt capability
from datetime import datetime
from alpaca_trade_api import REST
from timedelta import Timedelta
from finbert import get_sentiment

API_KEY_ID = creds.API_KEY_ID
API_SECRET_KEY = creds.API_SECRET_KEY
BASE_URL = creds.BASE_URL

ALPACA_CREDS = {
    "API_KEY" : API_KEY_ID,
    "API_SECRET" : API_SECRET_KEY,
    "PAPER" : True
}

CASH_AT_RISK = 0.5
START_DATE = datetime(2020,1,1)
END_DATE = datetime(2023,12,31)


class TradingStrategy(Strategy):
    """Contains the core strategy for the training bot"""

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

    def get_news_sentiment(self):
        days_prior, today = self.get_day_interval(3)
        news = self.api.get_news(self.symbol, start=days_prior, end=today)

        headlines = [ev.__dict__["_raw"]["headline"] for ev in news]
        #summaries = [ev.__dict__["_raw"]["summary"] for ev in news]

        probability, sentiment = get_sentiment(headlines)

        return probability, sentiment


    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_news_sentiment()

        if sentiment == "positive" and probability > .999: 
            if self.last_trade == "sell": 
                self.sell_all() 
            order = self.create_order(self.symbol,
                                        quantity,
                                        "buy",
                                        type="bracket",
                                        take_profit_price=last_price*1.20,
                                        stop_loss_price=last_price*.95)
            self.submit_order(order) 
            self.last_trade = "buy"

        elif sentiment == "negative" and probability > .999: 
            if self.last_trade == "buy": 
                self.sell_all() 
            order = self.create_order(self.symbol,
                                        quantity,
                                        "sell",
                                        type="bracket", 
                                        take_profit_price=last_price*.8, 
                                        stop_loss_price=last_price*1.05
                                        )
            self.submit_order(order) 
            self.last_trade = "sell"


broker = Alpaca(ALPACA_CREDS)
strategy = TradingStrategy(name="RocketTrader", broker=broker,
                           parameters={"symbol":"SPY", "cash_at_risk":CASH_AT_RISK})
strategy.backtest(YahooDataBacktesting, START_DATE, END_DATE,
                  parameters={"symbol":"SPY", "cash_at_risk":CASH_AT_RISK})



