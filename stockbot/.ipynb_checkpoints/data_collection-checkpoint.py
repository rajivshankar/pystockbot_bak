# data_collection.py
"""
This module creates the following data collection tools
"""
# import the key modules
import datetime as dt
import sys
import os
import time
import pickle
import logging

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web

logger = logging.getLogger(__name__)

NUM_YEARS = 5 # Choose the timeframe for the analysis

def get_start_end_dates(end_date=dt.datetime.today(), duration=dt.timedelta(days=365)*NUM_YEARS):
    '''
    gets the start and end dates of the analysis period based on the time duration
    '''
    logger.debug('Inside get_start_end_dates')
    
    end = dt.datetime(year=end_date.year, month=end_date.month, day=end_date.day)
    start = end - duration
    return start, end


def retrieve_existing_ticker_data(ticker, start, end):
    '''
    check the csv if it exists and if it does, if the data corresponds to the start and end dates
    If not, return an empty DataFrame
    '''
    logger.debug('Inside retrieve_existing_ticker_data')
    
    try:
        df = pd.read_csv('./data/stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)
        df.index = pd.to_datetime(df.index)
        
        logger.info('end_date: {0} and max_index: {1}'.format(end, df.index.max()))
        logger.info('start_date: {0} and min_index: {1}'.format(start, df.index.min()))
        
        if(end != df.index.max() or start != df.index.min()):
            logger.warning('Returning an empty dataframe')
            return pd.DataFrame()
        else:
            logger.info('Already have {}.csv'.format(ticker))
            return df
    except Exception as e:
        logger.info('Error whilst retrieving ticker[{0}]: {1}'.format(ticker, str(e)))
        return pd.DataFrame()
    

def ping_yahoo_for_ticker(ticker, start_date, end_date):
    '''
    get the yahoo data in a DataFrame for the ticker. if nothing is found return empty DataFrame
    '''
    logger.debug('Inside ping_yahoo_for_ticker')
    
    try:
        df = web.DataReader(ticker, 'yahoo', start_date, end_date)
        logger.debug('Successfully retrieved data for {}'.format(ticker))
        logger.debug(df.head())
        return df
    except Exception as e:
        logging.error('Error while accessing Yahoo - {}'.format(str(e)))
        return pd.DataFrame()


def get_ticker_data_from_yahoo(ticker):
    '''
    gets the ticker from yahoo apis for a given ticker
    '''
    logger.debug('Inside get_ticker_data_from_yahoo')
    
    if not os.path.exists('./data/stock_dfs'):
        os.makedirs('./data/stock_dfs')
    
    start_date, end_date = get_start_end_dates(end_date=dt.datetime.today(), duration=dt.timedelta(days=365)*NUM_YEARS)
    
    logger.debug('Start Date: {}'.format(dt.datetime.strftime(start_date, '%d/%m/%Y')))
    logger.debug('End Date: {}'.format(dt.datetime.strftime(end_date, '%d/%m/%Y')))

    logger.debug('Processing ticker: {}'. format(ticker))
    df = pd.DataFrame()
    df = retrieve_existing_ticker_data(ticker, start_date, end_date)
    if df.empty:
        df = ping_yahoo_for_ticker(ticker, start_date, end_date)
        if not df.empty:
            logger.info('Dumping data for {}'.format(ticker))
            df.to_csv('./data/stock_dfs/{}.csv'.format(ticker))
        else:
            logger.info('Yahoo returned Empty DataFrame')
    return df