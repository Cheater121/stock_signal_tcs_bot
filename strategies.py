from telebot import types
from setup_logger import logger

def levels_with_notification(stock, bot):
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
                if name.startswith('MA') and (target.endswith('LOW') or target.endswith('HIGH')):
                    continue
                
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
    