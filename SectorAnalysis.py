#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd


# In[4]:


import yfinance as yf


# In[5]:


import matplotlib.dates as mdates


# In[6]:


import datetime as dt


# In[7]:


import time


# In[8]:


import matplotlib.pyplot as plt


# In[9]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[10]:


import numpy as np


# In[11]:


import os
from os import listdir
from os.path import isfile, join


# In[12]:


import cufflinks as cf
import plotly.express as px
import plotly.graph_objects as go


# In[13]:


from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
# Use Plotly locally
cf.go_offline()


# In[14]:


from plotly.subplots import make_subplots


# In[15]:


import warnings
warnings.simplefilter("ignore")


# In[ ]:





# In[16]:


PATH = "D:/Python For Finance/Wilshire/"
S_DATE='2017-02-01'
E_DATE='2022-12-06'
S_DATE_DT=pd.to_datetime(S_DATE)
E_DATE_DT=pd.to_datetime(E_DATE)


# In[17]:


def get_stock_df_from_csv(ticker):
    try:
        df = pd.read_csv(PATH + ticker + '.csv', index_col=0)
    except FileNotFoundError:
        print("File Does Not Exist")
        return None  # It's good practice to return None or handle the error appropriately.
    else:
        return df


# In[18]:


def get_fill_color(label):
    if label >= 1:
        return 'rgba(0,250,0,0.4)'
    else:
        return 'rgba(250,0,0,0.4)'


# In[19]:


def get_Ichimoku(df):

    candle = go.Candlestick(x=df.index, open=df['Open'],
    high=df['High'], low=df["Low"], close=df['Close'], name="Candlestick")

    df1 = df.copy()
    fig = go.Figure()
    df['label'] = np.where(df['SpanA'] > df['SpanB'], 1, 0)
    df['group'] = df['label'].ne(df['label'].shift()).cumsum()

    df = df.groupby('group')

    dfs = []
    for name, data in df:
        dfs.append(data)

    for df in dfs:
        fig.add_traces(go.Scatter(x=df.index, y=df.SpanA,
        line=dict(color='rgba(0,0,0,0)')))

        fig.add_traces(go.Scatter(x=df.index, y=df.SpanB,
        line=dict(color='rgba(0,0,0,0)'),
        fill='tonexty',
        fillcolor=get_fill_color(df['label'].iloc[0])))

    baseline = go.Scatter(x=df1.index, y=df1['Baseline'], 
    line=dict(color='pink', width=2), name="Baseline")

    conversion = go.Scatter(x=df1.index, y=df1['Conversion'], 
    line=dict(color='black', width=1), name="Conversion")

    lagging = go.Scatter(x=df1.index, y=df1['Lagging'], 
    line=dict(color='purple', width=2), name="Lagging")

    span_a = go.Scatter(x=df1.index, y=df1['SpanA'], 
    line=dict(color='green', width=2, dash='dot'), name="Span A")

    span_b = go.Scatter(x=df1.index, y=df1['SpanB'], 
    line=dict(color='red', width=1, dash='dot'), name="Span B")

    fig.add_trace(candle)
    fig.add_trace(baseline)
    fig.add_trace(conversion)
    fig.add_trace(lagging)
    fig.add_trace(span_a)
    fig.add_trace(span_b)
    
    fig.update_layout(height=1200, width=1800, showlegend=True)

    fig.show()


# In[20]:


sec_df=pd.read_csv('D:/Python For Finance/big_stock_sectors.csv')
sec_df['Sector']
indus_df=sec_df.loc[sec_df['Sector']=='Industrial']
health_df=sec_df.loc[sec_df['Sector']=='Healthcare']
it_df=sec_df.loc[sec_df['Sector']=='Information Technology']
comm_df=sec_df.loc[sec_df['Sector']=='Communication']
staple_df=sec_df.loc[sec_df['Sector']=='Staples']
discretion_df=sec_df.loc[sec_df['Sector']=='Discretionary']
utility_df=sec_df.loc[sec_df['Sector']=='Utilities']
financial_df=sec_df.loc[sec_df['Sector']=='Financials']
material_df=sec_df.loc[sec_df['Sector']=='Materials']
restate_df=sec_df.loc[sec_df['Sector']=='Real Estate']


# In[21]:


def get_cum_ret_for_stocks(stock_df):
    tickers = []
    cum_rets = []

    for index, row in stock_df.iterrows():
        df = get_stock_df_from_csv(row['Ticker'])
        
        # Check if df is None or empty
        if df is None or df.empty:
            print(f"No data for ticker: {row['Ticker']}")
            continue  # Skip this ticker

        # Ensure 'cum_return' column exists
        if 'cum_return' in df.columns and not df['cum_return'].empty:
            cum = df['cum_return'].iloc[-1]
            tickers.append(row['Ticker'])
            cum_rets.append(cum)
        else:
            print(f"'cum_return' column is missing or empty for ticker: {row['Ticker']}")
            continue  # Skip this ticker

    return pd.DataFrame({'Ticker': tickers, 'CUM_RET': cum_rets})


# In[22]:


industrial = get_cum_ret_for_stocks(indus_df)
health_care = get_cum_ret_for_stocks(health_df)
it = get_cum_ret_for_stocks(it_df)
commun = get_cum_ret_for_stocks(comm_df)
staple = get_cum_ret_for_stocks(staple_df)
discretion = get_cum_ret_for_stocks(discretion_df)
utility = get_cum_ret_for_stocks(utility_df)
finance = get_cum_ret_for_stocks(financial_df)
material = get_cum_ret_for_stocks(material_df)
restate = get_cum_ret_for_stocks(restate_df)
#PLS SCROLL TILL END TO FIND TOP PERFORMING STOCKS BY SECTOR 


# # BEST PERFORMING INDUSTRIAL STOCKS

# In[75]:


industrial.sort_values(by=['CUM_RET'], ascending=False).head(10)


# In[25]:


df_ind = get_stock_df_from_csv("CALX")
get_Ichimoku(df_ind)


# # BEST PERFORMING HEALTH CARE STOCKS

# In[27]:


health_care.sort_values(by=['CUM_RET'], ascending=False).head(10)


# In[28]:


df_hc = get_stock_df_from_csv("LLY")
get_Ichimoku(df_hc)


# # BEST PERFORMING IT STOCKS

# In[74]:


it.sort_values(by=['CUM_RET'], ascending=False).head(10)


# In[31]:


df_it = get_stock_df_from_csv("NVDA")
get_Ichimoku(df_it)


# # BEST PERFORMING TELECOM STOCKS

# In[33]:


commun.sort_values(by=['CUM_RET'], ascending=False).head(10)


# In[34]:


df_com = get_stock_df_from_csv("NFLX")
get_Ichimoku(df_it)


# # BEST PERFORMING STAPLES STOCKS

# In[36]:


staple.sort_values(by=['CUM_RET'], ascending=False).head(10)


# In[37]:


df_stap = get_stock_df_from_csv("WMT")
get_Ichimoku(df_stap)


# # BEST PERFORMING DISCRETION STOCKS

# In[39]:


discretion.sort_values(by=['CUM_RET'], ascending=False).head(10)


# In[40]:


df_dis = get_stock_df_from_csv("LULU")
get_Ichimoku(df_dis)


# # BEST PERFORMING UTILITY STOCKS

# In[42]:


utility.sort_values(by=['CUM_RET'], ascending=False).head(10)


# In[43]:


df_utl = get_stock_df_from_csv("AWK")
get_Ichimoku(df_utl)


# # BEST PERFORMING FINANCIAL STOCKS

# In[45]:


finance.sort_values(by=['CUM_RET'], ascending=False).head(10)


# In[46]:


df_fin = get_stock_df_from_csv("KKR")
get_Ichimoku(df_fin)


# # BEST PERFORMING MATERIAL STOCKS

# In[48]:


material.sort_values(by=['CUM_RET'], ascending=False).head(10)


# In[49]:


df_mat = get_stock_df_from_csv("AVY")
get_Ichimoku(df_mat)


# # BEST PERFORMING REAL ESTATE STOCKS

# In[51]:


restate.sort_values(by=['CUM_RET'], ascending=False).head(10)


# In[52]:


df_re = get_stock_df_from_csv("CBRE")
get_Ichimoku(df_re)


# In[ ]:




