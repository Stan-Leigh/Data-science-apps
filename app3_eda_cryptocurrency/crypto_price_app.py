# This app is for educational purpose only. Insights gained is not financial advice. Use at your own risk!
import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import datetime
#---------------------------------#
# New feature (make sure to upgrade your streamlit library)
# pip install --upgrade streamlit

#---------------------------------#
# Page layout
## Page expands to full width
st.set_page_config(layout="wide")
#---------------------------------#
# Title

image = Image.open('logo.jpg')

st.image(image, use_column_width=True)

st.title('Cryptocurrency Price App')
# st.markdown("<h1 style='text-align: center;'>Cryptocurrency Price App</h1>", unsafe_allow_html=True)
st.markdown("""
This app retrieves historical cryptocurrency prices for the top 20 cryptocurrencies from **CoinMarketCap**!
""")
#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, datetime
* **Data source:** [CoinMarketCap](http://coinmarketcap.com).
* **Credit:** Web scraper adapted from Youtube *[Web Scrape or Gather the Top 10 Cryptocurrencies Data By Market Cap Using Python](https://www.youtube.com/watch?v=thHCp3TL6QE)*
""")


#---------------------------------#
# Page layout (continued)
## Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar
col2, col3 = st.columns((2,1))

#---------------------------------#
# Sidebar + Main panel
col1.header('Input Options')

## Sidebar - Currency price unit
# currency_price_unit = col1.selectbox('Select currency for price', ('USD', 'BTC', 'ETH'))

# calculate the previous sundays' date because that is the last time the historical data in cmc got updated. 
# the date is also in the link we are scraping from
today = datetime.date.today()
idx = (today.weekday() + 1) % 7
sun = today - datetime.timedelta(idx)
date = str(sun).replace('-', '')

# Web scraping of CoinMarketCap data
@st.cache
def load_data():

    # dataframe columns
    coin_name = []
    coin_symbol = []
    market_cap = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []
    price = []
    volume_24h = []

    # get the url
    url = 'https://coinmarketcap.com/historical/' + date + '/'

    # make a request to the website
    cmc = requests.get(url)

    # parse the text from the website
    soup = BeautifulSoup(cmc.text, 'html.parser')

    # get the table row element
    tr = soup.find_all('tr', attrs={'class': 'cmc-table-row'})

    # create a count variable for the number of crypto we want to scrape
    count = 0

    # loop through every row to gather data/information
    for row in tr:
        if count >= 20:
            break
        count += 1

        # store the name of the cryptocurrency into a variable
        # find the td element (or column) to later get the cryptocurrency name
        name_column = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name'})
        crypto_name = name_column.find('a', attrs={'class': 'cmc-table__column-name--name cmc-link'}).text.strip()
        crypto_symbol = name_column.find('a', attrs={'class': 'cmc-table__column-name--symbol cmc-link'}).text.strip()

        # market cap
        crypto_market_cap = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap'}).text.strip().lstrip('$').replace(',', '')

        # price
        crypto_price = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price'}).text.strip().lstrip('$').replace(',', '')

        # volume(24h)
        vol_column = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__volume-24-h'})
        crypto_volume = vol_column.find('a', attrs={'class': 'cmc-link'}).text.strip().lstrip('$').replace(',', '')

        # percent 1h
        percent_1h = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-1-h'})
        crypto_percent_1h = percent_1h.find('div', attrs={'class': 'cmc--change-negative'})
        if crypto_percent_1h is None:
            crypto_percent_1h = percent_1h.find('div', attrs={'class': 'cmc--change-positive'}).get_text().rstrip('%').replace(',', '')
        else:
            crypto_percent_1h = crypto_percent_1h.get_text().rstrip('%').replace(',', '')

        # percent 24h
        percent_24h = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-24-h'})
        crypto_percent_24h = percent_24h.find('div', attrs={'class': 'cmc--change-negative'})
        if crypto_percent_24h is None:
            crypto_percent_24h = percent_24h.find('div', attrs={'class': 'cmc--change-positive'}).get_text().rstrip('%').replace(',', '')
        else:
            crypto_percent_24h = crypto_percent_24h.get_text().rstrip('%').replace(',', '')

        # percent 7d
        percent_7d = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-7-d'})
        crypto_percent_7d = percent_7d.find('div', attrs={'class': 'cmc--change-negative'})
        if crypto_percent_7d is None:
            crypto_percent_7d = percent_7d.find('div', attrs={'class': 'cmc--change-positive'}).get_text().rstrip('%').replace(',', '')
        else:
            crypto_percent_7d = crypto_percent_7d.get_text().rstrip('%').replace(',', '')

        coin_name.append(crypto_name)
        coin_symbol.append(crypto_symbol)
        market_cap.append(crypto_market_cap)
        percent_change_24h.append(crypto_percent_24h)
        percent_change_7d.append(crypto_percent_7d)
        percent_change_1h.append(crypto_percent_1h)
        price.append(crypto_price)
        volume_24h.append(crypto_volume)

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h

    convert_dict = {'price': float, 'percent_change_1h': float, 'percent_change_24h': float, 'percent_change_7d': float, 'market_cap': float, 'volume_24h': float,}
    df = df.astype(convert_dict)
    return df

df = load_data()

## Sidebar - Cryptocurrency selections
sorted_coin = sorted( df['coin_symbol'] )
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[ (df['coin_symbol'].isin(selected_coin)) ] # Filtering data

## Sidebar - Number of coins to display
num_coin = col1.slider('Display Top N Coins', 1, 20, 20)
df_coins = df_selected_coin[:num_coin]

## Sidebar - Percent change timeframe
percent_timeframe = col1.selectbox('Percent change time frame',
                                    ['7d','24h', '1h'])
# percent_dict = {"7d":'percent_change_7d',"24h":'percent_change_24h',"1h":'percent_change_1h'}
# selected_percent_timeframe = percent_dict[percent_timeframe]

## Sidebar - Sorting values
sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

col2.subheader('Price Data of Selected Cryptocurrency')
col2.write('Data Dimension: ' + str(df_coins.shape[0]) + ' rows and ' + str(df_coins.shape[1]) + ' columns.')
col2.write('Date since last update: ' + str(sun.strftime("%B %d, %Y.")))

col2.dataframe(df_coins)

# Download CSV data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
    return href

col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

#---------------------------------#
# Preparing data for Bar plot of % Price change
col2.subheader('Table of % Price Change')
df_change = pd.concat([df_coins.coin_symbol, df_coins.percent_change_1h, df_coins.percent_change_24h, df_coins.percent_change_7d], axis=1)
df_change = df_change.set_index('coin_symbol')
df_change['positive_percent_change_1h'] = df_change['percent_change_1h'] > 0
df_change['positive_percent_change_24h'] = df_change['percent_change_24h'] > 0
df_change['positive_percent_change_7d'] = df_change['percent_change_7d'] > 0
col2.dataframe(df_change)

# Conditional creation of Bar plot (time frame)
col3.subheader('Bar plot of % Price Change')

if percent_timeframe == '7d':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_7d'])
    col3.write('***7 days period***')
    plt.figure(figsize=(5,14))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_7d'].plot(kind='barh', color=df_change.positive_percent_change_7d.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
elif percent_timeframe == '24h':
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_24h'])
    col3.write('***24 hour period***')
    plt.figure(figsize=(5,14))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_24h'].plot(kind='barh', color=df_change.positive_percent_change_24h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)
else:
    if sort_values == 'Yes':
        df_change = df_change.sort_values(by=['percent_change_1h'])
    col3.write('***1 hour period***')
    plt.figure(figsize=(5,14))
    plt.subplots_adjust(top = 1, bottom = 0)
    df_change['percent_change_1h'].plot(kind='barh', color=df_change.positive_percent_change_1h.map({True: 'g', False: 'r'}))
    col3.pyplot(plt)