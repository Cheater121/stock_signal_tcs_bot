"""ToDo:
- add the ability to search for an instrument by ticker
- add the ability to edit (add/remove) the list of tracked instruments
"""

import telebot

from telebot import custom_filters
from time import sleep
from tinkoff.invest import CandleInterval

from stocks.stock_info import stocks_list
from errors.setup_logger import logger
from strategies.strategies import levels_with_notification, rsi_notification, macd_notification, sma_hour_notification
from utils.timers import time_checker
from config_data.config import load_config

config = load_config()

TG_TOKEN = config.tg_bot.token

bot = telebot.TeleBot(TG_TOKEN)
bot.update_switcher = True


@bot.message_handler(is_chat_admin=True, commands=['start'])
def start_handler(message):
    try:
        bot.send_message(message.chat.id,
                         "Hello! Prepare for spam. To stop it use '/stop' command. And '/help' for all commands.")
        bot.chat_id = message.chat.id
        bot.update_switcher = True
        while bot.update_switcher:
            if time_checker():
                for stock in stocks_list:
                    sleep(1)  # Delay for Tinkoff API
                    stock.load_old_prices()  # load from database

                    # Run all strategies
                    stock.get_new_prices(interval=CandleInterval.CANDLE_INTERVAL_HOUR, days=100)
                    sma_hour_notification(stock, bot)
                    stock.get_new_prices()
                    levels_with_notification(stock, bot)
                    rsi_notification(stock, bot)
                    macd_notification(stock, bot)

                    stock.save_old_prices()  # save to database
            sleep(60)
    except Exception as e:
        logger.exception(f"Exception in start handler: \n{e}\n")


@bot.message_handler(is_chat_admin=True, commands=['stop'])
def stop_handler(message):
    try:
        bot.send_message(message.chat.id, "Bye bye! To start use '/start'.")
        bot.update_switcher = False
    except Exception as e:
        logger.exception(f"Exception in stop handler: \n{e}\n")


@bot.message_handler(is_chat_admin=True, commands=['status'])
def status_checker(message):
    try:
        if bot.update_switcher is True:
            on_off = "on"
        else:
            on_off = "off"
        bot.reply_to(message, f"I'm fine, thanks! Update switcher is {on_off}")
    except Exception as e:
        logger.exception(f"Exception in status checker:\n{e}\n")


@bot.message_handler(commands=['stocks'])
def stock_handler(message):
    try:
        tickers = []
        for stock in stocks_list:
            tickers.append(stock.ticker)
        answer = ", ".join(tickers)
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        logger.exception(f"Exception in stock handler: \n{e}\n")


@bot.message_handler(commands=['help'])
def help_handler(message):
    try:
        bot.send_message(message.chat.id,
                         "I have commands: '/start' (for admins), '/stop' (for admins), '/status' (for admins), "
                         "'/stocks' (for all members) - send tracked stocks list.")
    except Exception as e:
        logger.exception(f"Exception in help handler: \n{e}\n")


if __name__ == "__main__":
    while True:
        try:
            bot.add_custom_filter(custom_filters.IsAdminFilter(bot))
            bot.polling()
        except Exception as e:
            logger.exception(f"Exception in main cycle: \n{e}\n")
