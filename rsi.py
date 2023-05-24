import pandas as pd
import numpy as np


def RSI_object(candles_closes: list, period: int):
    series = pd.Series(candles_closes)
    delta = series.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period-1]] = np.mean( u[:period] )
    u = u.drop(u.index[:(period-1)])
    d[d.index[period-1]] = np.mean( d[:period] )
    d = d.drop(d.index[:(period-1)])
    rs = pd.DataFrame.ewm(u, com=period-1, adjust=False).mean() / \
         pd.DataFrame.ewm(d, com=period-1, adjust=False).mean()
    return 100 - 100 / (1 + rs)

def get_current_rsi(data: list) -> float:
    all_rsi = RSI_object(data, 14) #timeframe = 14 days
    last_index = all_rsi.last_valid_index()
    return all_rsi.get(last_index)

