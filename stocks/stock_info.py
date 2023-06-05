from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import now
from datetime import datetime, timedelta

from errors.setup_logger import logger
from strategies.rsi import get_current_rsi
from strategies.macd import get_macd
from strategies.moving_averages import get_ma
from strategies.interval_levels import get_interval_levels
from config_data.config import load_config
from models.models import db, Stock, Indicator

config = load_config()

TCS_TOKEN = config.tcs_client.token


class StockAnalyzer:
    # Support/resistance levels Strategy
    old_levels = {'PRICE': 0, 'MA20': 0, 'MA50': 0, 'MA100': 0, 'MA200': 0, 'YESTERDAY_LOW': 0, 'YESTERDAY_HIGH': 0,
                  'WEEK_LOW': 0, 'WEEK_HIGH': 0, 'MONTH_LOW': 0, 'MONTH_HIGH': 0}
    levels = {'PRICE': 0, 'MA20': 0, 'MA50': 0, 'MA100': 0, 'MA200': 0, 'YESTERDAY_LOW': 0, 'YESTERDAY_HIGH': 0,
              'WEEK_LOW': 0, 'WEEK_HIGH': 0, 'MONTH_LOW': 0, 'MONTH_HIGH': 0}

    # RSI Strategy
    old_rsi = None
    current_rsi = None

    # MACD Strategy
    old_macd = None
    old_macds = None
    macd = None
    macds = None

    # SMA 20/50 Strategy
    old_ma20_hour = None
    old_ma50_hour = None
    ma20_hour = None
    ma50_hour = None

    def __init__(self, figi: str, ticker: str):
        self.figi = figi
        self.ticker = ticker

    def get_new_prices(self, interval=CandleInterval.CANDLE_INTERVAL_DAY, days=300):
        try:
            timeframe = 'HOUR' if interval == CandleInterval.CANDLE_INTERVAL_HOUR else 'DAY'
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

    def _update_prices(self, close_price, close_prices, minimal_values, maximum_values, timeframe='DAY'):
        try:
            if timeframe == 'DAY':
                ma20, ma50, ma100, ma200 = get_ma(close_prices)
                month_low, month_high, week_low, week_high, prev_day_low, prev_day_high = get_interval_levels(
                    minimal_values, maximum_values)
                print(f'{self.ticker} MA20 = {ma20}', f'MA50 = {ma50}',
                      f'MA100 = {ma100}', f'MA200 = {ma200}', f'Price = {close_price}',
                      f'Previous day low = {prev_day_low}', f'Seven day low = {week_low}',
                      f'Month low = {month_low}', f'Previous day high = {prev_day_high}',
                      f'Seven day high = {week_high}', f'Month high = {month_high}')
                self.levels = {'PRICE': close_price, 'MA20': round(ma20, 2),
                               'MA50': round(ma50, 2), 'MA100': round(ma100, 2),
                               'MA200': round(ma200, 2), 'YESTERDAY_LOW': prev_day_low,
                               'YESTERDAY_HIGH': prev_day_high, 'WEEK_LOW': week_low, 'WEEK_HIGH': week_high,
                               'MONTH_LOW': month_low, 'MONTH_HIGH': month_high}
                self.current_rsi = get_current_rsi(close_prices)
                self.macd, self.macds = get_macd(close_prices)
            elif timeframe == 'HOUR':
                self.ma20_hour, self.ma50_hour, *_ = get_ma(close_prices)
                print(f'SMA20: {self.ma20_hour}, SMA50: {self.ma50_hour}')
            else:
                raise AssertionError
        except Exception as e:
            logger.exception(f"Exception in update prices method: \n{e}\n")

    def load_old_prices(self): # ToDo write this method
        try:
            pass
        except Exception as e:
            logger.exception(f"Exception in load old prices method: \n{e}\n")

    def save_old_prices(self):
        try:
            db.create_tables([Stock, Indicator])
        except Exception as e:
            logger.exception(f"Exception in create tables method: \n{e}\n")

        try:
            stock = Stock.select().where(Stock.ticker == self.ticker)
        except Exception as e:
            stock = Stock(ticker=self.ticker, figi=self.figi)
            stock.save()
            logger.exception(f"Exception in save stock method: \n{e}\n")

        try:
            indicators = Indicator(price=self.old_levels.get("PRICE"),
                                   from_stock=stock,
                                   ma20=self.old_levels.get("MA20"),
                                   ma50=self.old_levels.get("MA50"),
                                   ma100=self.old_levels.get("MA100"),
                                   ma200=self.old_levels.get("MA200"),
                                   yesterday_low=self.old_levels.get("YESTERDAY_LOW"),
                                   yesterday_high=self.old_levels.get("YESTERDAY_HIGH"),
                                   week_low=self.old_levels.get("WEEK_LOW"),
                                   week_high=self.old_levels.get("WEEK_HIGH"),
                                   month_low=self.old_levels.get("MONTH_LOW"),
                                   month_high=self.old_levels.get("MONTH_HIGH"),
                                   rsi=self.old_rsi,
                                   macd=self.old_macd,
                                   macds=self.old_macds,
                                   ma20_hour=self.old_ma20_hour,
                                   ma50_hour=self.old_ma50_hour,
                                   date=datetime.now())
            indicators.save()
        except Exception as e:
            logger.exception(f"Exception in save old prices (indicators) method: \n{e}\n")


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
