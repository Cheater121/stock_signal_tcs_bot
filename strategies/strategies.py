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
                    print(f'{name} ({new.get(name)} rub.) down {target} ({new.get(target)} rub.)')
                    bot.send_message(bot.chat_id,
                                     f"{attention}${stock.ticker} <b>{name}</b> ({new.get(name)} руб.) breakdown "
                                     f"support <b>{target}</b> ({new.get(target)} руб.) \U0001F534{attention}",
                                     parse_mode="HTML", reply_markup=bot.keyboard1)
                    sleep(4)
                # buy
                if old.get(name) < old.get(target) and new.get(name) > new.get(target):
                    print(f'{name} ({new.get(name)} rub.) up {target} ({new.get(target)} rub.)')
                    bot.send_message(bot.chat_id,
                                     f"{attention}${stock.ticker} <b>{name}</b> ({new.get(name)} руб.) break upward "
                                     f"resistance <b>{target}</b> ({new.get(target)} руб.){attention} \U0001F7E2",
                                     parse_mode="HTML", reply_markup=bot.keyboard1)
                    sleep(4)
        for indicator in priority_list:
            stock.old_levels[indicator] = stock.levels.get(indicator)
    except Exception as e:
        logger.exception(f"Exception in sort levels method: \n{e}\n")


def rsi_notification(stock, bot):
    try:
        bot.keyboard1 = types.InlineKeyboardMarkup()
        url_btn = types.InlineKeyboardButton(text=f"{stock.ticker}",
                                             url=f"https://www.tinkoff.ru/invest/stocks/{stock.ticker}")
        bot.keyboard1.add(url_btn)
        
        old_rsi = stock.old_levels.get("RSI")
        current_rsi = stock.levels.get("RSI")
        # attention to sell
        if old_rsi and old_rsi < 70 < current_rsi:
            attention = "\U000026A0"
            print(f'RSI is overbought ({current_rsi}), be careful!')
            bot.send_message(bot.chat_id,
                             f"{attention}${stock.ticker} <b>RSI</b> is overbought ({round(current_rsi, 2)}), "
                             f"be careful!{attention}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        # sell
        if old_rsi and old_rsi > 70 > current_rsi:
            attention = "\U0000203C"
            print(f'RSI cross downward 70 ({current_rsi}), time to sell!')
            bot.send_message(bot.chat_id,
                             f"{attention}${stock.ticker} <b>RSI</b> cross downward 70 ({round(current_rsi, 2)}), "
                             f"time to sell!\U0001F534{attention}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        # attention to buy
        if old_rsi and old_rsi > 30 > current_rsi:
            attention = "\U000026A0"
            print(f'RSI is oversold ({current_rsi}), be careful!')
            bot.send_message(bot.chat_id,
                             f"{attention}${stock.ticker} <b>RSI</b> is oversold ({round(current_rsi, 2)}), be "
                             f"careful!{attention}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        # buy
        if old_rsi and old_rsi < 30 < current_rsi:
            attention = "\U0000203C"
            print(f'RSI cross upward 30 ({current_rsi}), time to buy!')
            bot.send_message(bot.chat_id,
                             f"{attention}${stock.ticker} <b>RSI</b> cross upward 30 ({round(current_rsi, 2)}), "
                             f"time to buy!\U0001F7E2{attention}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        stock.old_levels["RSI"] = stock.levels.get("RSI")
    except Exception as e:
        logger.exception(f"Exception in rsi method: \n{e}\n")


def macd_notification(stock, bot):
    try:
        bot.keyboard1 = types.InlineKeyboardMarkup()
        url_btn = types.InlineKeyboardButton(text=f"{stock.ticker}",
                                             url=f"https://www.tinkoff.ru/invest/stocks/{stock.ticker}")
        bot.keyboard1.add(url_btn)
        
        old_macd = stock.old_levels.get("MACD")
        macd = stock.levels.get("MACD")
        old_macds = stock.old_levels.get("MACDs")
        macds = stock.levels.get("MACDs")
        # buy
        if old_macd and old_macd < old_macds and macd > macds:
            attention = "\U0000203C"
            print('MACD cross upward the signal line MACDs, time to buy!')
            bot.send_message(bot.chat_id,
                             f"{attention}${stock.ticker} <b>MACD</b> cross upward the signal line "
                             f"MACDs!\U0001F7E2{attention}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        # sell
        if old_macd and old_macd > old_macds and macd < macds:
            attention = "\U0000203C"
            print('MACD cross downward the signal line MACDs, time to sell!')
            bot.send_message(bot.chat_id,
                             f"{attention}${stock.ticker} <b>MACD</b> cross downward the signal "
                             f"line MACDs!\U0001F534{attention}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        stock.old_levels["MACD"], stock.old_levels["MACDs"] = stock.levels.get("MACD"), stock.levels.get("MACDs")
    except Exception as e:
        logger.exception(f"Exception in rsi method: \n{e}\n")
 
               
def sma_hour_notification(stock, bot):
    try:
        bot.keyboard1 = types.InlineKeyboardMarkup()
        url_btn = types.InlineKeyboardButton(text=f"{stock.ticker}",
                                             url=f"https://www.tinkoff.ru/invest/stocks/{stock.ticker}")
        bot.keyboard1.add(url_btn)
        
        old_ma20_hour = stock.old_levels.get("MA20_HOUR")
        ma20_hour = stock.levels.get("MA20_HOUR")
        old_ma50_hour = stock.old_levels.get("MA50_HOUR")
        ma50_hour = stock.levels.get("MA50_HOUR")
        # buy
        if old_ma20_hour and old_ma20_hour < old_ma50_hour and ma20_hour > ma50_hour:
            attention = "\U0000203C"
            print('HOUR SMA20 cross upward SMA50, time to buy!')
            bot.send_message(bot.chat_id,
                             f"{attention*3}${stock.ticker} <b>HOUR SMA20</b> cross upward "
                             f"SMA50!\U0001F7E2{attention*3}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        # sell
        if old_ma20_hour and old_ma20_hour > old_ma50_hour and ma20_hour < ma50_hour:
            attention = "\U0000203C"
            print('HOUR SMA20 cross downward SMA50, time to sell!')
            bot.send_message(bot.chat_id,
                             f"{attention*3}${stock.ticker} <b>HOUR SMA20</b> cross downward "
                             f"SMA50!\U0001F534{attention*3}",
                             parse_mode="HTML", reply_markup=bot.keyboard1)
            sleep(4)
        stock.old_levels["MA20_HOUR"], stock.old_levels["MA50_HOUR"] = stock.levels.get("MA20_HOUR"), stock.levels.get("MA50_HOUR")
    except Exception as e:
        logger.exception(f"Exception in rsi method: \n{e}\n")
        