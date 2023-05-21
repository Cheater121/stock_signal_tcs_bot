'''ToDo: 
- add the ability to search for an instrument by ticker 
- add the ability to edit (add/remove) the list of tracked instruments 
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
        attention = ""
        old = stock.old
        new = stock.new
        priority_list = ['PRICE', 'MA20', 'MA50', 'MA100', 'MA200', 'YESTERDAY_LOW', 'YESTERDAY_HIGH', 'WEEK_LOW', 'WEEK_HIGH', 'MONTH_LOW', 'MONTH_HIGH']
        for i in range(len(priority_list)):
            name = priority_list[i]
            if name != 'PRICE':
                attention = '\U0000203C'
            for target in priority_list[i+1::]:
                bot.keyboard1 = types.InlineKeyboardMarkup()
                url_btn = types.InlineKeyboardButton(text=f"{stock.ticker}", url=f"https://www.tinkoff.ru/invest/stocks/{stock.ticker}")
                bot.keyboard1.add(url_btn)
                if old.get(name) > old.get(target) and new.get(name) < new.get(target):
                    print(f'{name} ({new.get(name)} rub.) vniz {target} ({new.get(target)} rub.)')
                    bot.send_message(bot.chat_id, f"{attention}${stock.ticker} <b>{name}</b> ({new.get(name)} руб.) breakdown support <b>{target}</b> ({new.get(target)} руб.) \U0001F534{attention}", parse_mode="HTML", reply_markup=bot.keyboard1)
                if old.get(name) < old.get(target) and new.get(name) > new.get(target):
                    print(f'{name} ({new.get(name)} rub.) vverh {target} ({new.get(target)} rub.)')
                    bot.send_message(bot.chat_id, f"{attention}${stock.ticker} <b>{name}</b> ({new.get(name)} руб.) break upward resistance <b>{target}</b> ({new.get(target)} руб.){attention} \U0001F7E2", parse_mode="HTML", reply_markup=bot.keyboard1)
        stock.old = stock.new
    except Exception as e:
        logger.exception(f"Exeption in sort method: \n{e}\n")
    

@bot.message_handler(commands=['start'], chat_types=['supergroup'], is_chat_admin=True)
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

@bot.message_handler(commands=['stop'], chat_types=['supergroup'], is_chat_admin=True)
def stop_handler(message):
    try:
        bot.send_message(message.chat.id, "Bye bye! To start use '/start'.")
        bot.update_switcher = False
    except Exception as e:
        logger.exception(f"Exeption in stop handler: \n{e}\n")
    
@bot.message_handler(commands=['status'], chat_types=['supergroup'], is_chat_admin=True)
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

@bot.message_handler(commands=['help'], chat_types=['supergroup'], is_chat_admin=True)
def help_handler(message):
    try:
        bot.send_message(message.chat.id, "I have commands: '/start', '/stop', '/status', '/stocks'.")
    except Exception as e:
        logger.exception(f"Exeption in help handler: \n{e}\n")

                

if __name__ == "__main__":
    print("start")
    bot.polling()
    print("finished")

