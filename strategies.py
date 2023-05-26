from telebot import types
from setup_logger import logger
from time import sleep

def levels_with_notification(stock, bot):
    try:
        old = stock.old
        new = stock.new
        priority_list = ['PRICE', 'MA20', 'MA50', 'MA100', 'MA200', 'YESTERDAY_LOW', 'YESTERDAY_HIGH', 'WEEK_LOW', 'WEEK_HIGH', 'MONTH_LOW', 'MONTH_HIGH']
        for i in range(len(priority_list)):
            name = priority_list[i]
            for target in priority_list[i+1::]:
                if name.startswith('MA') and (target.endswith('LOW') or target.endswith('HIGH')):
                    continue
                attention = ""
                if name.startswith('MA') and target.startswith('MA'):
                    attention = '\U0000203C'
                    
                bot.keyboard1 = types.InlineKeyboardMarkup()
                url_btn = types.InlineKeyboardButton(text=f"{stock.ticker}", url=f"https://www.tinkoff.ru/invest/stocks/{stock.ticker}")
                bot.keyboard1.add(url_btn)
                # sell
                if old.get(name) > old.get(target) and new.get(name) < new.get(target):
                    print(f'{name} ({new.get(name)} rub.) vniz {target} ({new.get(target)} rub.)')
                    bot.send_message(bot.chat_id, f"{attention}${stock.ticker} <b>{name}</b> ({new.get(name)} руб.) breakdown support <b>{target}</b> ({new.get(target)} руб.) \U0001F534{attention}", parse_mode="HTML", reply_markup=bot.keyboard1)
                    sleep(1)
                # buy
                if old.get(name) < old.get(target) and new.get(name) > new.get(target):
                    print(f'{name} ({new.get(name)} rub.) vverh {target} ({new.get(target)} rub.)')
                    bot.send_message(bot.chat_id, f"{attention}${stock.ticker} <b>{name}</b> ({new.get(name)} руб.) break upward resistance <b>{target}</b> ({new.get(target)} руб.){attention} \U0001F7E2", parse_mode="HTML", reply_markup=bot.keyboard1)
                    sleep(1)
        stock.old = stock.new
    except Exception as e:
        logger.exception(f"Exeption in sort levels method: \n{e}\n")

def rsi_notification(stock, bot):
    try:
        bot.keyboard1 = types.InlineKeyboardMarkup()
        url_btn = types.InlineKeyboardButton(text=f"{stock.ticker}", url=f"https://www.tinkoff.ru/invest/stocks/{stock.ticker}")
        bot.keyboard1.add(url_btn)
        # attention to sell
        if stock.old_rsi is not None and stock.old_rsi < 70 and stock.current_rsi > 70:
            attention = "\U000026A0"
            print(f'RSI is overbought ({stock.current_rsi}), be careful!')
            bot.send_message(bot.chat_id, f"{attention}${stock.ticker} <b>RSI</b> is overbought ({round(stock.current_rsi, 2)}), be careful!{attention}", parse_mode="HTML", reply_markup=bot.keyboard1)
        # sell
        if stock.old_rsi is not None and stock.old_rsi > 70 and stock.current_rsi < 70:
            attention = "\U0000203C"
            print(f'RSI cross downward 70 ({stock.current_rsi}), time to sell!')
            bot.send_message(bot.chat_id, f"{attention}${stock.ticker} <b>RSI</b> cross downward 70 ({round(stock.current_rsi, 2)}), time to sell!\U0001F534{attention}", parse_mode="HTML", reply_markup=bot.keyboard1)
        # attention to buy
        if stock.old_rsi is not None and stock.old_rsi > 30 and stock.current_rsi < 30:
            attention = "\U000026A0"
            print(f'RSI is oversold ({stock.current_rsi}), be careful!')
            bot.send_message(bot.chat_id, f"{attention}${stock.ticker} <b>RSI</b> is oversold ({round(stock.current_rsi, 2)}), be careful!{attention}", parse_mode="HTML", reply_markup=bot.keyboard1)
        # buy
        if stock.old_rsi is not None and stock.old_rsi < 30 and stock.current_rsi > 30:
            attention = "\U0000203C"
            print(f'RSI cross upward 30 ({stock.current_rsi}), time to buy!')
            bot.send_message(bot.chat_id, f"{attention}${stock.ticker} <b>RSI</b> cross upward 30 ({round(stock.current_rsi, 2)}), time to buy!\U0001F7E2{attention}", parse_mode="HTML", reply_markup=bot.keyboard1)
        stock.old_rsi = stock.current_rsi
    except Exception as e:
        logger.exception(f"Exeption in rsi method: \n{e}\n")

def macd_notification(stock, bot):
    try:
        bot.keyboard1 = types.InlineKeyboardMarkup()
        url_btn = types.InlineKeyboardButton(text=f"{stock.ticker}", url=f"https://www.tinkoff.ru/invest/stocks/{stock.ticker}")
        bot.keyboard1.add(url_btn)
        # buy
        if stock.old_macd is not None and stock.old_macd < stock.macds and stock.macd > stock.macds:
            attention = "\U0000203C"
            print('MACD cross upward the signal line MACDs, time to buy!')
            bot.send_message(bot.chat_id, f"{attention}${stock.ticker} <b>MACD</b> cross upward the signal line MACDs!\U0001F7E2{attention}", parse_mode="HTML", reply_markup=bot.keyboard1)
        # sell
        if stock.old_macd is not None and stock.old_macd > stock.old_macds and stock.macd < stock.macds:
            attention = "\U0000203C"
            print('MACD cross downward the signal line MACDs, time to sell!')
            bot.send_message(bot.chat_id, f"{attention}${stock.ticker} <b>MACD</b> cross downward the signal line MACDs!\U0001F534{attention}", parse_mode="HTML", reply_markup=bot.keyboard1)
        stock.old_macd, stock.old_macds = stock.macd, stock.macds
    except Exception as e:
        logger.exception(f"Exeption in rsi method: \n{e}\n")

        