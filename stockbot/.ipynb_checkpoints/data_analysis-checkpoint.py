# data_analysis.py

import pandas as pd

'''
Quick Reference Guide for Buying
================================

1) Check the Major Trend in the overall Market
2) Uncover the few groups that look the best technically
3) Make a list of those stocks in the favourable groups that have a bullish pattern, but are now in trading ranges. Write down the price at which you expect each stock to breakout
4) Narrow the list. Discard those that have overhead resistance nearby
5) Narrow down your list further by checking Relative Strength (RS)
6) Put in your buy-stop orders for half of your positions for those few stocks that meet your buying criteria. Use buy-stop orders on a good-'til-cancel (GTC) basis
7) If the volume is favourable on the breakout, buy the other half position on the pull back to initial breakout
8) If the volume pattern is negative (not high enough during intial breakout), sell the stock on first rally. if it fails to rally, but falls back to the initial breakout point, immediately dump it
'''

'''
Stan's DONT'T Commandments
~~~~~~~~~~~~~~~~~~~~~~~~~~

* Don't buy when the overall market sentiment is bearish
* Don't buuy stock in a negative group
* Don't buy stock below its 30-week Moving Average (MA)
* Don't buy stock on a declining 30-week MA, even if its price is trending above the said MA
* No matter how bullish a stock is, don't buy a stock too late into an advance when it is far above its ideal entry point
* Don't buy stock that has poor volume characterstics on the breakout. If you bought it because you had a buy-stop order, sell it quickly
* Don't buy stock showing poor Relative Strength (RS)
* Don't buy stock that has heavy nearby overhead resistance
* Don't guess a bottom. what looks like a bargain can turn out to be a very expensive Stage 4 disaster. Instead buy on breakouts above resistance
'''

