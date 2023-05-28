def get_ma(close_prices: list):
    sum_ma20, sum_ma50, sum_ma100, sum_ma200 = 0, 0, 0, 0
    for i in range(len(close_prices)):
        # get sum for calculate MA200
        if len(close_prices) - i <= 200:
            sum_ma200 += close_prices[i]
        # get sum for calculate MA100
        if len(close_prices) - i <= 100:
            sum_ma100 += close_prices[i]
        # get sum for calculate MA50
        if len(close_prices) - i <= 50:
            sum_ma50 += close_prices[i]
        # get sum for calculate MA20
        if len(close_prices) - i <= 20:
            sum_ma20 += close_prices[i]
    return sum_ma20/20, sum_ma50/50, sum_ma100/100, sum_ma200/200
