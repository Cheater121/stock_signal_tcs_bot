import pandas as pd
import pandas_ta as ta


def get_macd(close_prices: list):
    df = pd.DataFrame(close_prices, dtype='float')
    df.rename(columns={0: 'close'}, inplace=True)
    
    # Calculate MACD values using the pandas_ta library
    df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
    
    # View result
    # pd.set_option("display.max_columns", None) # show all columns
    
    # Get MACD
    last_index = df.last_valid_index()
    macd = df['MACD_12_26_9'].values[last_index]
    macds = df['MACDs_12_26_9'].values[last_index]
    
    return macd, macds
