import telebot
from datetime import timedelta
from time import sleep

import tokens
from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import now

#import os
#TCS_TOKEN = os.environ["INVEST_TOKEN"]
#TG_TOKEN = os.environ["'TELEGRAM_BOT_TOKEN'"]
TCS_TOKEN = tokens.TCS_TOKEN
TG_TOKEN = tokens.TG_TOKEN


bot = telebot.TeleBot(TG_TOKEN)
@bot.message_handler(commands=['start'])
def start_handler(message):
	bot.send_message(message.chat.id, "Hello! Prepare for spam.")
	bot.chat_id = message.chat.id
	ozon = Stock("BBG00Y91R9T3", "OZON")
	sber = Stock("BBG004730N88", "SBER")
	stocks = [ozon, sber]
	while True:
		for stock in stocks:
			stock.get_new_prices()
			stock.sort_with_notification()
		sleep(30)

@bot.message_handler(commands=['stop'])
def stop_handler(message):
	bot.send_message(message.chat.id, "Bye bye!")
	bot.stop_polling()


class Stock:
	old = [('price', 0), ('ma20', 1), ('ma50', 2), ('ma100', 3), ('ma200', 4)]
	new = [('price', 5), ('ma20', 10), ('ma50', 1), ('ma100', 3), ('ma200', 2)]
	
	
	def __init__(self, figi, ticker):
		self.figi = figi
		self.ticker = ticker
	
	def sort_with_notification(self):
		self.old.sort(key=lambda x: x[1])
		self.new.sort(key=lambda x: x[1])
		for i in range(5):
			if self.new[i][0] != self.old[i][0]:
				for j in range(4, -1, -1):
					if self.old[j][0] == self.new[i][0] and j != i:
						print(f"{self.ticker} {self.old[j][0]} пробило вверх {self.old[j-1][0]}")
						bot.send_message(bot.chat_id, f"{self.ticker} {self.old[j][0]} пробило вверх {self.old[j-1][0]}")
						self.old[j], self.old[j-1] = self.old[j-1], self.old[j]
		self.old = self.new
	
	def get_new_prices(self):
	   with Client(TCS_TOKEN) as client:
	       ma20, ma50, ma100, ma200, counter = 0, 0, 0, 0, 0
	       for candle in client.get_all_candles(figi=self.figi, from_=now() - timedelta(days=200), interval=CandleInterval.CANDLE_INTERVAL_DAY):
	           counter += 1
	           #print(candle, "\n")
	           close_price = candle.close.units + candle.close.nano/(10**9)
	           if counter > 0:
	           	ma200 += close_price
	           if counter > 100:
	           	ma100 += close_price
	           if counter > 150:
	           	ma50 += close_price
	           if counter > 180:
	           	ma20 += close_price
	       print(counter, f'{self.ticker} MA20 = {ma20/(counter-180)}', f'MA50 = {ma50/(counter-150)}', f'MA100 = {ma100/(counter-100)}', f'MA200 = {ma200/counter}', f'Price = {close_price}')
	       self.new = [('ma20', round(ma20/(counter-180)), 2), ('ma50', round(ma50/(counter-150)), 2), ('ma100', round(ma100/(counter-100)), 2), ('ma200', round(ma200/counter), 2), ('price', close_price)]
	       print(self.new)


if __name__ == "__main__":
	print("start")
	bot.polling()
	print("finished")

