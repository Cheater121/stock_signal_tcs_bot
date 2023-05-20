'''ToDo: 
- add the ability to search for an instrument by ticker 
- add the ability to edit (add/remove) the list of tracked instruments 
- make a system of priorities for indicators (where something breaks through) - rewrite sort_with_notifications function
'''

import os
import dotenv
import telebot

from telebot import types
from time import sleep
from stock_info import stocks_list
from setup_logger import logger



dotenv.load_dotenv()

TG_TOKEN = os.getenv('TG_TOKEN')


bot = telebot.TeleBot(TG_TOKEN)
bot.update_switcher = True

def sort_with_notification(stock):
        try:
            stock.old.sort(key=lambda x: x[1])
            stock.new.sort(key=lambda x: x[1])
            for i in range(5):
                if stock.new[i][0] != stock.old[i][0]:
                    for j in range(4, -1, -1):
                        if stock.old[j][0] == stock.new[i][0] and j != i:
                            if stock.old[j][1] != 0:
                                for t in stock.new:
                                    if t[0] == stock.old[j-1][0]:
                                        price = t[1]
                                print(f"{stock.ticker} {stock.old[j][0]} ({stock.new[i][1]} руб.) пробило вниз {stock.old[j-1][0]} ({price} руб.)")
                                bot.keyboard1 = types.InlineKeyboardMarkup()
                                url_btn = types.InlineKeyboardButton(text=f"{stock.ticker}", url=f"https://www.tinkoff.ru/invest/stocks/{stock.ticker}")
                                bot.keyboard1.add(url_btn)
                                if stock.old[j][0] == "PRICE" or stock.old[j-1][0] == "PRICE":
                                    bot.send_message(bot.chat_id, f"{stock.ticker} <b>{stock.old[j][0]}</b> ({stock.new[i][1]} руб.) пробило вниз <b>{stock.old[j-1][0]}</b> ({price} руб.)", parse_mode="HTML", reply_markup=bot.keyboard1)
                                else:
                                    bot.send_message(bot.chat_id, f"\U0000203C {stock.ticker} <b>{stock.old[j][0]}</b> ({stock.new[i][1]} руб.) пробило вниз <b>{stock.old[j-1][0]}</b> ({price} руб.) \U0000203C", parse_mode="HTML", reply_markup=bot.keyboard1)                                
                            stock.old[j], stock.old[j-1] = stock.old[j-1], stock.old[j]
            stock.old = stock.new
        except Exception as e:
            logger.exception(f"Exeption in sort method: \n{e}\n")

@bot.message_handler(commands=['start'])
def start_handler(message):
    try:
        bot.send_message(message.chat.id, "Hello! Prepare for spam. To stop it use '/stop' command. And '/help' for all commands.")
        bot.chat_id = message.chat.id
        bot.update_switcher = True
        while bot.update_switcher is True:
            for stock in stocks_list:
                stock.get_new_prices()
                sort_with_notification(stock)
            sleep(60*60)
    except Exception as e:
        logger.exception(f"Exeption in start handler: \n{e}\n")

@bot.message_handler(commands=['stop'])
def stop_handler(message):
    try:
        bot.send_message(message.chat.id, "Bye bye! To start use '/start'.")
        bot.update_switcher = False
    except Exception as e:
        logger.exception(f"Exeption in stop handler: \n{e}\n")
    
@bot.message_handler(commands=['status'])
def status_checker(message):
    try:
        if bot.update_switcher is True:
            on_off = "on"
        else:
            on_off = "off"
        bot.reply_to(message, f"I'm fine, thanks! Update swithcer is {on_off}")
    except Exception as e:
        logger.exception(f"Exeption in status checker:\n{e}\n")

@bot.message_handler(commands=['stocks'])
def stock_handler(message):
    try:
        bot.send_message(message.chat.id, "OZON, SBER, SGZH, POLY, VKCO, TATN, NVTK, SPBE, NLMK, PIKK, FIVE, AFKS, YNDX, ROSN, ALRS, GMKN, AFLT, GAZP, LKOH, MOEX")
    except Exception as e:
        logger.exception(f"Exeption in stock handler: \n{e}\n")

@bot.message_handler(commands=['help'])
def help_handler(message):
    try:
        bot.send_message(message.chat.id, "I have commands: '/start', '/stop', '/status', '/stocks'.")
    except Exception as e:
        logger.exception(f"Exeption in help handler: \n{e}\n")

                

if __name__ == "__main__":
    print("start")
    bot.polling()
    print("finished")

