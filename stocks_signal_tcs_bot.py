import os
import dotenv
import telebot

from telebot import types
from datetime import timedelta
from time import sleep

from tinkoff.invest import CandleInterval, Client
from tinkoff.invest.utils import now


dotenv.load_dotenv()

TCS_TOKEN = os.environ["TCS_TOKEN"]
TG_TOKEN = os.environ["'TG_TOKEN'"]


bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start'])
def start_handler(message):
	bot.send_message(message.chat.id, "Hello! Prepare for spam. To stop it use '/stop' command. And '/help' for all commands.")
	bot.chat_id = message.chat.id
	bot.update_switcher = True
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
	stocks = [ozon, sber, sgzh, poly, vkco, tatn, nvtk, spbe, nlmk, pikk, five, afks, yndx, rosn, alrs, gmkn, aflt, gazp, lkoh, moex]
	while bot.update_switcher is True:
		for stock in stocks:
			stock.get_new_prices()
			stock.sort_with_notification()
		sleep(60*60)

@bot.message_handler(commands=['stop'])
def stop_handler(message):
	bot.send_message(message.chat.id, "Bye bye! To start use '/start'.")
	bot.update_switcher = False
	
@bot.message_handler(commands=['status'])
def status_checker(message):
	if bot.update_switcher is True:
		on_off = "on"
	else:
		on_off = "off"
	bot.reply_to(message, f"I'm fine, thanks! Update swithcer is {on_off}")

@bot.message_handler(commands=['stocks'])
def stock_handler(message):
	bot.send_message(message.chat.id, "OZON, SBER, SGZH, POLY, VKCO, TATN, NVTK, SPBE, NLMK, PIKK, FIVE, AFKS, YNDX, ROSN, ALRS, GMKN, AFLT, GAZP, LKOH, MOEX")

@bot.message_handler(commands=['help'])
def help_handler(message):
	bot.send_message(message.chat.id, "I have commands: '/start', '/stop', '/status', '/stocks'.")



class Stock:
	old = [('price', 0), ('ma20', 0), ('ma50', 0), ('ma100', 0), ('ma200', 0)]
	new = [('price', 5), ('ma20', 10), ('ma50', 1), ('ma100', 3), ('ma200', 2)]
	
	
	def __init__(self, figi: str, ticker: str):
		self.figi = figi
		self.ticker = ticker
	
	def sort_with_notification(self):
		self.old.sort(key=lambda x: x[1])
		self.new.sort(key=lambda x: x[1])
		for i in range(5):
			if self.new[i][0] != self.old[i][0]:
				for j in range(4, -1, -1):
					if self.old[j][0] == self.new[i][0] and j != i:
						if self.old[j][1] != 0:
							for t in self.new:
								if t[0] == self.old[j-1][0]:
									price = t[1]
							print(f"{self.ticker} {self.old[j][0]} ({self.new[i][1]} руб.) пробило вниз {self.old[j-1][0]} ({price} руб.)")
							bot.keyboard1 = types.InlineKeyboardMarkup()
							url_btn = types.InlineKeyboardButton(text=f"{self.ticker}", url=f"https://www.tinkoff.ru/invest/stocks/{self.ticker}")
							bot.keyboard1.add(url_btn)
							if self.old[j][0] == "price" or self.old[j-1][0] == "price":
								bot.send_message(bot.chat_id, f"{self.ticker} {self.old[j][0]} ({self.new[i][1]} руб.) пробило вниз {self.old[j-1][0]} ({price} руб.)", reply_markup=bot.keyboard1)
							else:
								bot.send_message(bot.chat_id, f"\U0000203C {self.ticker} {self.old[j][0]} ({self.new[i][1]} руб.) пробило вниз {self.old[j-1][0]} ({price} руб.) \U0000203C", reply_markup=bot.keyboard1)								
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
	       #print(self.new)


if __name__ == "__main__":
	print("start")
	bot.polling()
	print("finished")

