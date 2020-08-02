# preprocessing.py
"""
This module prepares the data based on which the whole analysis works
"""
import sys
import logging
import pandas as pd
import numpy as np

SMA_WEEKS_LIST = [10, 30]
NUM_WEEKS_LIST = [1, 2, 3]
NUM_MONTHS_LIST = [1, 3, 6, 12, 36, 60]

from . import data_collection as dc

logger = logging.getLogger(__name__)


def mark_trend_turn(x):
    if (x[0] <= 0 and x[1] > 0):
        return 1
    elif (x[0] != 0 and x[1] == 0):
        return 0
    elif (x[0] >= 0 and x[1] < 0):
        return -1
    else:
        return np.NaN


def calculate_MA_Trends(df, df_base):
    for num_weeks in SMA_WEEKS_LIST:
        df[f'SMA {num_weeks:02d}W'] = df_base['Adj Close'].rolling(window=7*num_weeks, min_periods=1).mean()
        
        df[f'Trend SMA {num_weeks:02d}W'] = df[f'SMA {num_weeks:02d}W'].rolling(window=2).aggregate(lambda x: round((x[1] - x[0]) / x[0], 4))
        df[f'Trend SMA {num_weeks:02d}W'] = df[f'Trend SMA {num_weeks:02d}W'].fillna(0)
        
        # to determine when the trend in MA changes from positive to neutral or to negative and vice versa
        df[f'Stage Trend {num_weeks:02d}W'] = df[f'Trend SMA {num_weeks:02d}W'].rolling(window=2).apply(mark_trend_turn)

        

def calculate_volume_trends(df, df_base, ticker):
    df['{} Volume'.format(ticker)] = df_base['Volume']
    df['Volume SMA 30D'] = df_base['Volume'].rolling(window=30, min_periods=1).mean()
    
        
def calculate_dorsey_relative_strength(df, ticker, index_ticker):
    '''
    Calculates the Dorsey Relative Strenth using the historical data of the ticker and index_ticker
    '''
    df['RSD'] = (df['{} Adj Close'.format(ticker)] / df['{} Adj Close'.format(index_ticker)]) * 100
    

def calculate_mansfield_relative_strength(df, ticker, index_ticker):
    """
    Calculates the Mansfield Relative Strength of the stock based on the value of Dorsey RS
    given by the key 'RSD' in the data frame
    """
    calculate_dorsey_relative_strength(df, ticker, index_ticker)
    try:
        df['RSM'] = ((df['RSD'] / df['RSD'].rolling(window=7*52, min_periods=1).mean()) - 1) * 100
    except Exception as e:
        logging.error('Error while computing RSM - {}'.format(str(e)))


def compare_price_history_by_month(df, ticker, num_months=1):
    key_ticker_price = '{} Adj Close'.format(ticker)
    key_price_history = f'Price History {num_months:03d}M'
    df[key_price_history] = df[key_ticker_price] == df[key_ticker_price].rolling(window=30*num_months, min_periods=1).max()
    

def compare_price_history_by_week(df, ticker, num_weeks=1):
    key_ticker_price = '{} Adj Close'.format(ticker)
    key_price_history = f'Price History {num_weeks:d}W'
    df[key_price_history] = df[key_ticker_price] == df[key_ticker_price].rolling(window=7*num_weeks, min_periods=1).max()
    

def prepare_analytical_data(ticker, index_ticker):
    """
    retrieve the data from yahoo and prepare the base data dataframe
    """
    df_base = dc.get_ticker_data_from_yahoo(ticker)
    df_index = dc.get_ticker_data_from_yahoo(index_ticker)
    
    if df_base.empty:
        return pd.DataFrame()
    
    df = pd.DataFrame()
    
    df['{} Adj Close'.format(ticker)] = df_base['Adj Close']
    
    calculate_MA_Trends(df, df_base)
    
    calculate_volume_trends(df, df_base, ticker)

    df['{} Adj Close'.format(index_ticker)] = df_index['Adj Close']
    
    calculate_mansfield_relative_strength(df, ticker, index_ticker)
    
    '''
    calculate if the current price was exceeded in the last week, month,
    quarter, half-year, year, 3 years and 5 years 
    '''
    for num_weeks in NUM_WEEKS_LIST:
        compare_price_history_by_week(df, ticker, num_weeks)
    
    for num_months in NUM_MONTHS_LIST:
        compare_price_history_by_month(df, ticker, num_months)
    
    return df


