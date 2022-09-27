import yfinance as yf
import streamlit as st

st.write("""
# Simple Stock Price App
This app shows the closing prices and trading volumes of some of the most popular companies stocks.
***
""")

st.sidebar.header('User Input')
ticker = st.sidebar.selectbox('Company stock symbol', ['GOOGL', 'MSFT', 'AAPL', 'ADBE', 'NFLX', 'META', 'AMZN'])
start = st.sidebar.selectbox('Start date', ['2010-1-01', '2011-1-01', '2012-1-01', '2013-1-01', '2014-1-01', '2015-1-01'])
end = st.sidebar.selectbox('End date', ['2016-12-31', '2017-12-31', '2018-12-31', '2019-12-31', '2020-12-31', '2021-12-31'])

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
# define the ticker symbol
tickerSymbol = ticker
# get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
# get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start=start, end=end)
# Open	High	Low	Close	Volume	Dividends	Stock Splits

st.write("""
## Closing Price (Daily)
""")
st.line_chart(tickerDf.Close)
st.write("""
## Trading volume (Daily)
""")
st.line_chart(tickerDf.Volume)