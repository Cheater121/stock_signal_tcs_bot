import os
import dotenv
from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import now
from datetime import timedelta

from setup_logger import logger


dotenv.load_dotenv()

TCS_TOKEN = os.getenv("TCS_TOKEN")


class Stock:
    old = {'PRICE': 0, 'MA20': 0, 'MA50': 0, 'MA100': 0, 'MA200': 0, 'YESTERDAY_LOW': 0, 'YESTERDAY_HIGH': 0, 'WEEK_LOW': 0, 'WEEK_HIGH': 0, 'MONTH_LOW': 0, 'MONTH_HIGH': 0}
    new = {'PRICE': 0, 'MA20': 0, 'MA50': 0, 'MA100': 0, 'MA200': 0, 'YESTERDAY_LOW': 0, 'YESTERDAY_HIGH': 0, 'WEEK_LOW': 0, 'WEEK_HIGH': 0, 'MONTH_LOW': 0, 'MONTH_HIGH': 0}
    
    
    def __init__(self, figi: str, ticker: str):
        self.figi = figi
        self.ticker = ticker
    
    def get_new_prices(self):
       try:
           with Client(TCS_TOKEN) as client:
               ma20, ma50, ma100, ma200, counter = 0, 0, 0, 0, 0
               seven_day_low = 10**9
               month_low = 10**9
               seven_day_high = -1
               month_high = -1
               for candle in client.get_all_candles(figi=self.figi, from_=now() - timedelta(days=200), interval=CandleInterval.CANDLE_INTERVAL_DAY):
                   counter += 1
                   #print(candle, "\n")
                   close_price = candle.close.units + candle.close.nano/(10**9)
                   if counter > 0:
                       ma200 += close_price
                       if candle.is_complete is True:
                           prev_day_low = candle.low.units + candle.low.nano/(10**9)
                           prev_day_high = candle.high.units + candle.high.nano/(10**9)
                   if counter > 100:
                       ma100 += close_price
                   if counter > 150:
                       ma50 += close_price
                   if counter > 180:
                       ma20 += close_price
                   if counter > 170:
                       if candle.low.units + candle.low.nano/(10**9) < month_low:
                           month_low = candle.low.units + candle.low.nano/(10**9)
                       if candle.high.units + candle.high.nano/(10**9) > month_high:
                           month_high = candle.high.units + candle.high.nano/(10**9)
                   if counter > 193:
                       if candle.low.units + candle.low.nano/(10**9) < seven_day_low:
                           seven_day_low = candle.low.units + candle.low.nano/(10**9)
                       if candle.high.units + candle.high.nano/(10**9 > seven_day_high):
                           seven_day_high = candle.high.units + candle.high.nano/(10**9)
               print(counter, f'{self.ticker} MA20 = {ma20/(counter-180)}', f'MA50 = {ma50/(counter-150)}', f'MA100 = {ma100/(counter-100)}', f'MA200 = {ma200/counter}', f'Price = {close_price}', f'Previous day low = {prev_day_low}', f'Seven day low = {seven_day_low}', f'Month low = {month_low}', f'Previous day high = {prev_day_high}', f'Seven day high = {seven_day_high}', f'Month high = {month_high}')
               self.new = {'PRICE': close_price, 'MA20': round(ma20/(counter-180), 2), 'MA50': round(ma50/(counter-150), 2), 'MA100': round(ma100/(counter-100), 2), 'MA200': round(ma200/counter, 2), 'YESTERDAY_LOW': prev_day_low, 'YESTERDAY_HIGH': prev_day_high, 'WEEK_LOW': seven_day_low, 'WEEK_HIGH': seven_day_high, 'MONTH_LOW': month_low, 'MONTH_HIGH': month_high}
               #print(self.new)
       except Exception as e:
            logger.exception(f"Exeption in get prices method: \n{e}\n")


ozon = Stock("BBG00Y91R9T3", "OZON")
sber = Stock("BBG004730N88", "SBER")
sgzh = Stock("BBG0100R9963", "SGZH")
poly = Stock("BBG004PYF2N3", "POLY")
vkco = Stock("BBG00178PGX3", "VKCO")
tatn = Stock("BBG004RVFFC0", "TATN")
nvtk = Stock("BBG00475KKY8", "NVTK")
spbe = Stock("BBG002GHV6L9", "SPBE")
nlmk = Stock("BBG004S681B4", "NLMK")
pikk = Stock("BBG004S68BH6", "PIKK")
five = Stock("BBG00JXPFBN0", "FIVE")
afks = Stock("BBG004S68614", "AFKS")
yndx = Stock("BBG006L8G4H1", "YNDX")
rosn = Stock("BBG004731354", "ROSN")
alrs = Stock("BBG004S68B31", "ALRS")
gmkn = Stock("BBG004731489", "GMKN")
aflt = Stock("BBG004S683W7", "AFLT")
gazp = Stock("BBG004730RP0", "GAZP")
lkoh = Stock("BBG004731032", "LKOH")
moex = Stock("BBG004730JJ5", "MOEX")

stocks_list = [ozon, sber, sgzh, poly, vkco, tatn, nvtk, spbe, nlmk, pikk, five, afks, yndx, rosn, alrs, gmkn, aflt, gazp, lkoh, moex]

