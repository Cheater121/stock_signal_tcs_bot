from telebot import types
from errors.setup_logger import logger
from time import sleep


def levels_with_notification(stock, bot):
    try:
        old = stock.old_levels
        new = stock.levels
        priority_list = ['PRICE', 'MA20', 'MA50', 'MA100', 'MA200', 'YESTERDAY_LOW', 'YESTERDAY_HIGH', 'WEEK_LOW',
                         'WEEK_HIGH', 'MONTH_LOW', 'MONTH_HIGH']
        for i in range(len(priority_list)):
            name = priority_list[i]
            for target in priority_list[i + 1::]:
                if name.startswith('MA') and (target.endswith('LOW') or target.endswith('HIGH')):
                    continue
                attention = ""
                if name.startswith('MA') and target.startswith('MA'):
                    attention = '\U0000203C'

                bot.keyboard1 = types.InlineKeyboardMarkup()
                url_btn = types.InlineKeyboardButton(text=f"{stock.ticker}",
                                                     url=f"https://www.tinkoff.ru/invest/stocks/{stock.ticker}")
                bot.keyboard1.add(url_btn)
                # sell
                if old.get(name) > old.get(target) and new.get(name) < new.get(target):
                    print(f'{name} ({new.get(name)} rub.) vniz {target} ({new.get(target)} rub.)')
                    bot.send_message(bot.chat_id,
                                     f"{attention}${stock.ticker} <b>{name}</b> ({new.get(name)} руб.) breakdown "
                                     f"support <b>{target}</b> ({new.get(target)} руб.) \U0001F534{attention}",
                                     parse_mode="HTML", reply_markup=bot.keyboard1)
                    sleep(4)
                # buy
                if old.get(name) < old.get(target) and new.get(name) > new.get(target):
                    print(f'{name} ({new.get(name)} rub.) vverh {target} ({new.get(target)} rub.)')
                    bot.send_message(bot.chat_id,
                                     f"{attention}${stock.ticker} <b>{name}</b> ({new.get(name)} руб.) break upward "
                                     f"resistance <b>{target}</b> ({new.get(target)} руб.){attention} \U0001F7E2",
                                     parse_mode="HTML", reply_markup=bot.keyboard1)
                    sleep(4)
        stock.old_levels = stock.levels
    except Exception as e:
        logger.exception(f"Exception in sort levels method: \n{e}\n")


def rsi_notification(stock, bot):
    try:
        bot.keyboard1 = types.InlineKeyboardMarkup()
        url_btn = types.InlineKeyboardButton(text=f"{stock.ticker}",
                                             url=f"https://www.tinkoff.ru/invest/stocks/{stock.ticker}")
        bot.keyboard1.add(url_btn)
        # attention to sell
        if stock.old_rsi and stock.old_rsi < 70 < stock.current_rsi:
            attention = "\U000026A0"
            print(f'RSI is overbought ({stock.current_rsi}), be careful!')
            bot.send_message(bot.chat_id,
                             f"{attention}${stock.ticker} <b>RSI</b> is overbought ({round(stock.current_rsi, 2)}), "
                             f"be careful!{attention}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        # sell
        if stock.old_rsi and stock.old_rsi > 70 > stock.current_rsi:
            attention = "\U0000203C"
            print(f'RSI cross downward 70 ({stock.current_rsi}), time to sell!')
            bot.send_message(bot.chat_id,
                             f"{attention}${stock.ticker} <b>RSI</b> cross downward 70 ({round(stock.current_rsi, 2)}), time to sell!\U0001F534{attention}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        # attention to buy
        if stock.old_rsi and stock.old_rsi > 30 > stock.current_rsi:
            attention = "\U000026A0"
            print(f'RSI is oversold ({stock.current_rsi}), be careful!')
            bot.send_message(bot.chat_id,
                             f"{attention}${stock.ticker} <b>RSI</b> is oversold ({round(stock.current_rsi, 2)}), be "
                             f"careful!{attention}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        # buy
        if stock.old_rsi and stock.old_rsi < 30 < stock.current_rsi:
            attention = "\U0000203C"
            print(f'RSI cross upward 30 ({stock.current_rsi}), time to buy!')
            bot.send_message(bot.chat_id,
                             f"{attention}${stock.ticker} <b>RSI</b> cross upward 30 ({round(stock.current_rsi, 2)}), "
                             f"time to buy!\U0001F7E2{attention}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        stock.old_rsi = stock.current_rsi
    except Exception as e:
        logger.exception(f"Exception in rsi method: \n{e}\n")


def macd_notification(stock, bot):
    try:
        bot.keyboard1 = types.InlineKeyboardMarkup()
        url_btn = types.InlineKeyboardButton(text=f"{stock.ticker}",
                                             url=f"https://www.tinkoff.ru/invest/stocks/{stock.ticker}")
        bot.keyboard1.add(url_btn)
        # buy
        if stock.old_macd and stock.old_macd < stock.old_macds and stock.macd > stock.macds:
            attention = "\U0000203C"
            print('MACD cross upward the signal line MACDs, time to buy!')
            bot.send_message(bot.chat_id,
                             f"{attention}${stock.ticker} <b>MACD</b> cross upward the signal line MACDs!\U0001F7E2{attention}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        # sell
        if stock.old_macd and stock.old_macd > stock.old_macds and stock.macd < stock.macds:
            attention = "\U0000203C"
            print('MACD cross downward the signal line MACDs, time to sell!')
            bot.send_message(bot.chat_id,
                             f"{attention}${stock.ticker} <b>MACD</b> cross downward the signal line MACDs!\U0001F534{attention}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        stock.old_macd, stock.old_macds = stock.macd, stock.macds
    except Exception as e:
        logger.exception(f"Exception in rsi method: \n{e}\n")
 
               
def sma_hour_notification(stock, bot):
    try:
        bot.keyboard1 = types.InlineKeyboardMarkup()
        url_btn = types.InlineKeyboardButton(text=f"{stock.ticker}",
                                             url=f"https://www.tinkoff.ru/invest/stocks/{stock.ticker}")
        bot.keyboard1.add(url_btn)
        # buy
        if stock.old_ma20_hour and stock.old_ma20_hour < stock.old_ma50_hour and stock.ma20_hour > stock.ma50_hour:
            attention = "\U0000203C"
            print('HOUR SMA20 cross upward SMA50, time to buy!')
            bot.send_message(bot.chat_id,
                             f"{attention*3}${stock.ticker} <b>HOUR SMA20</b> cross upward SMA50!\U0001F7E2{attention*3}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        # sell
        if stock.old_ma20_hour and stock.old_ma20_hour > stock.old_ma50_hour and stock.ma20_hour < stock.ma50_hour:
            attention = "\U0000203C"
            print('HOUR SMA20 cross downward SMA50, time to sell!')
            bot.send_message(bot.chat_id,
                             f"{attention*3}${stock.ticker} <b>HOUR SMA20</b> cross downward SMA50!\U0001F534{attention*3}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        stock.old_ma20_hour, stock.old_ma50_hour = stock.ma20_hour, stock.ma50_hour
    except Exception as e:
        logger.exception(f"Exception in rsi method: \n{e}\n")
        