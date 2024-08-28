import creds
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime
from alpaca_trade_api import REST
from timedelta import Timedelta
from finbert import get_sentiment

# API credentials for Alpaca broker.
API_KEY_ID = creds.API_KEY_ID
API_SECRET_KEY = creds.API_SECRET_KEY
BASE_URL = creds.BASE_URL

# Alpaca broker credentials configuration.
ALPACA_CREDS = {
    "API_KEY": API_KEY_ID,
    "API_SECRET": API_SECRET_KEY,
    "PAPER": True  # Use paper trading (simulated trading environment).
}

# Backtesting time period.
START_DATE = datetime(2020, 1, 1)
END_DATE = datetime(2023, 12, 31)

# Percentage of cash to risk per trade.
CASH_AT_RISK = 0.5

class MLTrader(Strategy):
    """Machine Learning-based trading strategy that uses sentiment analysis.

    Attributes:
        symbol (str): The stock symbol to trade (e.g., "SPY").
        sleeptime (str): Time interval between trading iterations.
        last_trade (str or None): Tracks the type of the last trade ("buy" or "sell").
        cash_at_risk (float): The proportion of available cash to risk per trade.
        api (REST): Alpaca REST API client for fetching news and stock data.
    """

    def initialize(self, symbol: str = "SPY", cash_at_risk: float = 0.5):
        """Initializes the strategy with the stock symbol and cash at risk.

        Args:
            symbol (str): The stock symbol to trade. Defaults to "SPY".
            cash_at_risk (float): The proportion of cash to risk on each trade. Defaults to 0.5.
        """
        self.symbol = symbol
        self.sleeptime = "24H"
        self.last_trade = None
        self.cash_at_risk = cash_at_risk
        self.api = REST(key_id=API_KEY_ID, secret_key=API_SECRET_KEY, base_url=BASE_URL)

    def position_sizing(self):
        """Calculates the position size for the next trade.

        Returns:
            Tuple[float, float, int]: A tuple containing available cash, last price of the stock,
            and the quantity of shares to trade.
        """
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price, 0)
        return cash, last_price, quantity

    def get_dates(self):
        """Calculates the current date and the date three days prior.

        Returns:
            Tuple[str, str]: A tuple containing today's date and the date three days prior,
            both formatted as strings ('YYYY-MM-DD').
        """
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    def get_news_sentiment(self):
        """Fetches news articles and analyzes their sentiment.

        Returns:
            Tuple[float, str]: A tuple containing the probability of the predicted sentiment
            and the corresponding sentiment label ('positive', 'negative', or 'neutral').
        """
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=three_days_prior, end=today)
        news = [ev.__dict__["_raw"]["headline"] for ev in news]
        probability, sentiment = get_sentiment(news)
        return probability, sentiment

    def on_trading_iteration(self):
        """Executes a trading iteration based on sentiment analysis and position sizing.

        This function is called on each iteration of the trading loop. It fetches the
        current market data, analyzes the news sentiment, and makes buy or sell
        decisions based on predefined rules.
        """
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_news_sentiment()

        if cash > last_price:
            if sentiment == "positive" and probability > 0.999:
                if self.last_trade == "sell":
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price * 1.20,
                    stop_loss_price=last_price * 0.95
                )
                self.submit_order(order)
                self.last_trade = "buy"

            elif sentiment == "negative" and probability > 0.999:
                if self.last_trade == "buy":
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    "sell",
                    type="bracket",
                    take_profit_price=last_price * 0.80,
                    stop_loss_price=last_price * 1.05
                )
                self.submit_order(order)
                self.last_trade = "sell"

# Initialize the Alpaca broker using provided credentials.
broker = Alpaca(ALPACA_CREDS)

# Instantiate the MLTrader strategy with the specified parameters.
strategy = MLTrader(
    name='mlstrat',
    broker=broker,
    parameters={"symbol": "SPY", "cash_at_risk": CASH_AT_RISK}
)

# Run backtesting using historical data from Yahoo Finance.
strategy.backtest(
    YahooDataBacktesting,
    START_DATE,
    END_DATE,
    parameters={"symbol": "SPY", "cash_at_risk": CASH_AT_RISK}
)