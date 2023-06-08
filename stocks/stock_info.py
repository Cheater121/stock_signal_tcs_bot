from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import now
from datetime import timedelta

from errors.setup_logger import logger
from strategies.rsi import get_current_rsi
from strategies.macd import get_macd
from strategies.moving_averages import get_ma
from strategies.interval_levels import get_interval_levels
from config_data.config import load_config
from db.methods import database_connector

config = load_config()

TCS_TOKEN = config.tcs_client.token


class StockAnalyzer:

    def __init__(self, figi: str, ticker: str):
        self.figi = figi
        self.ticker = ticker
        self.old_levels = {"PRICE": 0, "MA20": 0, "MA50": 0, "MA100": 0, "MA200": 0, "YESTERDAY_LOW": 0,
                           "YESTERDAY_HIGH": 0, "WEEK_LOW": 0, "WEEK_HIGH": 0, "MONTH_LOW": 0, "MONTH_HIGH": 0,
                           "RSI": None, "MACD": None, "MACDs": None, "MA20_HOUR": None, "MA50_HOUR": None}
        self.levels = {"PRICE": 0, "MA20": 0, "MA50": 0, "MA100": 0, "MA200": 0, "YESTERDAY_LOW": 0,
                       "YESTERDAY_HIGH": 0, "WEEK_LOW": 0, "WEEK_HIGH": 0, "MONTH_LOW": 0, "MONTH_HIGH": 0,
                       "RSI": None, "MACD": None, "MACDs": None, "MA20_HOUR": None, "MA50_HOUR": None}

    def get_new_prices(self, interval=CandleInterval.CANDLE_INTERVAL_DAY, days=300):
        try:
            timeframe = "HOUR" if interval == CandleInterval.CANDLE_INTERVAL_HOUR else "DAY"
            with Client(TCS_TOKEN) as client:
                close_prices = []
                minimal_values = []
                maximum_values = []
                for candle in client.get_all_candles(figi=self.figi, from_=now() - timedelta(days=days),
                                                     interval=interval):
                    # print(candle, "\n")
                    close_price = candle.close.units + candle.close.nano / (10 ** 9)
                    close_prices.append(close_price)
                    if candle.is_complete:
                        minimal_values.append(candle.low.units + candle.low.nano / (10 ** 9))
                        maximum_values.append(candle.high.units + candle.high.nano / (10 ** 9))
                self._update_prices(close_price, close_prices, minimal_values, maximum_values, timeframe)
        except Exception as e:
            logger.exception(f"Exception in get prices method: \n{e}\n")

    def _update_prices(self, close_price, close_prices, minimal_values, maximum_values, timeframe="DAY"):
        try:
            if timeframe == "DAY":
                ma20, ma50, ma100, ma200 = get_ma(close_prices)
                month_low, month_high, week_low, week_high, prev_day_low, prev_day_high = get_interval_levels(
                    minimal_values, maximum_values)
                rsi = get_current_rsi(close_prices)
                macd, macds = get_macd(close_prices)
                self.levels["PRICE"] = close_price
                self.levels["MA20"] = round(ma20, 2)
                self.levels["MA50"] = round(ma50, 2)
                self.levels["MA100"] = round(ma100, 2)
                self.levels["MA200"] = round(ma200, 2)
                self.levels["YESTERDAY_LOW"] = prev_day_low
                self.levels["YESTERDAY_HIGH"] = prev_day_high
                self.levels["WEEK_LOW"] = week_low
                self.levels["WEEK_HIGH"] = week_high
                self.levels["MONTH_LOW"] = month_low
                self.levels["MONTH_HIGH"] = month_high
                self.levels["RSI"] = rsi
                self.levels["MACD"] = macd
                self.levels["MACDs"] = macds
                print(f"{self.ticker} {self.levels}")
            elif timeframe == "HOUR":
                self.levels["MA20_HOUR"], self.levels["MA50_HOUR"], *_ = get_ma(close_prices)
            else:
                raise AssertionError
        except Exception as e:
            logger.exception(f"Exception in update prices method: \n{e}\n")

    def save_old_prices(self):
        database_connector.save_old_prices(ticker=self.ticker, figi=self.figi, old_levels=self.old_levels)

    def load_old_prices(self):
        old_prices_from_db = database_connector.load_old_prices(ticker=self.ticker, figi=self.figi)
        if old_prices_from_db:
            for indicator in self.old_levels:
                self.old_levels[indicator] = old_prices_from_db[indicator]


ozon = StockAnalyzer("BBG00Y91R9T3", "OZON")
sber = StockAnalyzer("BBG004730N88", "SBER")
sgzh = StockAnalyzer("BBG0100R9963", "SGZH")
poly = StockAnalyzer("BBG004PYF2N3", "POLY")
vkco = StockAnalyzer("BBG00178PGX3", "VKCO")
tatn = StockAnalyzer("BBG004RVFFC0", "TATN")
nvtk = StockAnalyzer("BBG00475KKY8", "NVTK")
spbe = StockAnalyzer("BBG002GHV6L9", "SPBE")
nlmk = StockAnalyzer("BBG004S681B4", "NLMK")
pikk = StockAnalyzer("BBG004S68BH6", "PIKK")
five = StockAnalyzer("BBG00JXPFBN0", "FIVE")
afks = StockAnalyzer("BBG004S68614", "AFKS")
yndx = StockAnalyzer("BBG006L8G4H1", "YNDX")
rosn = StockAnalyzer("BBG004731354", "ROSN")
alrs = StockAnalyzer("BBG004S68B31", "ALRS")
gmkn = StockAnalyzer("BBG004731489", "GMKN")
aflt = StockAnalyzer("BBG004S683W7", "AFLT")
gazp = StockAnalyzer("BBG004730RP0", "GAZP")
lkoh = StockAnalyzer("BBG004731032", "LKOH")
moex = StockAnalyzer("BBG004730JJ5", "MOEX")

stocks_list = [ozon, sber, sgzh, poly, vkco, tatn, nvtk, spbe, nlmk, pikk, five, afks, yndx, rosn, alrs, gmkn, aflt,
               gazp, lkoh, moex]
