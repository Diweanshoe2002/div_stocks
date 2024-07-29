import numpy as np
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
import streamlit as st
from yfinance import Ticker
import gspread
import yfinance as yf
from nsedt import equity as eq
import pandas as pd
import pandas_ta as ta
import requests
from nsepython import *
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import sqlite3
import mplfinance as mpf
import json
import matplotlib.collections as collections
import datetime
from matplotlib.gridspec import GridSpec
from io import StringIO
st.set_page_config(page_title=None, page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
selected = option_menu(menu_title=None, options=["HOMEPAGE", "STOCK", "EVENT CALENDER", "DEALS", "NEWS"], icons=["house-fill", "graph-up-arrow", "calendar3","newspaper"],
                       orientation="horizontal")
#def add_bg_from_url():
#    st.markdown(
#         f"""
#         <style>
#         .stApp {{
#           background-image: url("https://cdn.pixabay.com/photo/2023/02/08/08/50/frequency-wave-7776034_1280.jpg");
#            background-attachment: fixed;
#           background-size: cover
#         }}
#         </style>
#         """,unsafe_allow_html=True)

#add_bg_from_url()
def nse_headers_session(url):
    baseurl = "https://www.nseindia.com/"
    headers = {"Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36",
    "Sec-Fetch-User": "?1", "Accept": "*/*", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate",
    "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9,hi;q=0.8"
    }
    request = requests.get(baseurl, headers=headers)
    #cookies = dict(request.cookies)
    response = requests.get(url, headers=headers)
    raw = (response.text)
    return raw


if selected == "HOMEPAGE":
    col1, col2, col3 = st.columns(3)
    col1.metric("NIFTY-50"," "," ")
    g2 = "^NSEI"
    info = Ticker(g2).history(period='1d', interval='5m',actions=False)
    info1 = pd.DataFrame(info)
    info1 = info1.reset_index(['Datetime'])
    info1.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    info1['date'] = pd.to_datetime(info1['date'], unit='s')
    fig = go.Figure(go.Scatter(
        x=info1['date'],
        y=info1["close"],
        mode='lines',
        line=dict(width=2, color='#0066CC'),
        showlegend=False
    ))
    fig.update_layout(width=200, height=50, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis={'visible': False},
            yaxis={'visible': False},margin=dict(t=0, b=0, l=0, r=0))
    config = {'displayModeBar': False}
    with col1:
        st.plotly_chart(fig, config=config)


    col2.metric("BANKNIFTY"," "," ")
    g3 = "^NSEBANK"
    info3 = Ticker(g3).history(period='1d', interval='5m',actions=False)
    info13 = pd.DataFrame(info3)
    info13 = info13.reset_index(['Datetime'])
    info13.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    info13['date'] = pd.to_datetime(info1['date'], unit='s')
    fig2 = go.Figure(go.Scatter(
        x=info13['date'],
        y=info13["close"],
        mode='lines',
        line=dict(width=2, color='#0066CC'),
        showlegend=False
    ))
    fig2.update_layout(
        width=200,
        height=50,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis={'visible': False },
        yaxis={'visible': False },
        margin=dict(t=0, b=0, l=0, r=0)
    )
    config = {'displayModeBar': False}
    with col2:
        st.plotly_chart(fig2, config=config)

    ty=(nse_get_index_quote("INDIA VIX"))

    col3.metric("INDIA VIX"," "," ")
    g4 = "^INDIAVIX"
    info4 = Ticker(g4).history(period='1d', interval='5m',actions=False)
    info14 = pd.DataFrame(info4)
    info14 = info14.reset_index(['Datetime'])
    info14.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    info14['date'] = pd.to_datetime(info1['date'], unit='s')
    fig3 = go.Figure(go.Scatter(
        x=info14['date'],
        y=info14["close"],
        mode='lines',
        line=dict(width=2, color='#0066CC'),
        showlegend=False
     ))
    fig3.update_layout(width=200, height=50, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis={'visible': False},
    yaxis={'visible': False}, margin=dict(t=0, b=0, l=0, r=0))
    config = {'displayModeBar': False}
    with col3:
        st.plotly_chart(fig3, config=config)

    col66,col77=st.columns(2)
    with col66:
        st.subheader("FII/DII DATA")
        sheet_id = "1T79XwzC8sG7pMHaNXYug9BJ9uwseBtLbrLM0G4seBAc"
        sheet_name = "Sheet4"
        link = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name)
        fiidii = pd.read_csv(link)
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.dataframe(fiidii)
    with col77:
        fiidii['buyValue'] = pd.to_numeric(fiidii['buyValue'])
        fiidii['sellValue'] = pd.to_numeric(fiidii['sellValue'])
        fiidii['netValue'] = pd.to_numeric(fiidii['netValue'])
        fig = px.bar(fiidii, x="category", y=["buyValue", "sellValue", "netValue"],barmode='group', height=320,width=580)
        fig.update_traces(textfont_size=16, textposition="outside", cliponaxis=False)
        fig.update_layout(bargap=0.5)
        st.plotly_chart(fig)

    sheet_id = "1T79XwzC8sG7pMHaNXYug9BJ9uwseBtLbrLM0G4seBAc"
    sheet_name = "Sheet7"
    link = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name)
    index = pd.read_csv(link)
    fig1 = px.treemap(index, path=[px.Constant("INDEXES"), 'key', 'indexSymbol'], values="last", color="percentChange")
    fig1.data[0].textinfo = 'label+text+value'
    fig1.update_traces(marker=dict(cornerradius=10))
    st.header("INDEX HEATMAP")
    col33, col44, col55=st.columns(3)
    fig1.update_layout(autosize=False, width=1200, height=550)
    st.plotly_chart(fig1)


    sheet_id = "1T79XwzC8sG7pMHaNXYug9BJ9uwseBtLbrLM0G4seBAc"
    sheet_name = "Sheet8"
    link = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name)
    upper = pd.read_csv(link)
    upperdf = pd.DataFrame(upper)
    st.write("UPPER CURCUIT STOCKS")
    pb=st.selectbox("PRICEBAND", upperdf['priceBand'].unique())
    upperdf = (upperdf[upperdf['series'] == "EQ"])
    st.dataframe(upperdf[upperdf['priceBand'].isin([pb])])

    sheet_name = "Sheet9"
    link1 = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name)
    lower = pd.read_csv(link1)
    lowerdf = pd.DataFrame(lower)
    st.write("LOWER CURCUIT STOCKS")
    lb=st.selectbox("priceband", lowerdf['priceBand'].unique())
    lowerdf = (lowerdf[lowerdf['series'] == "EQ"])
    st.dataframe(lowerdf[lowerdf['priceBand'].isin([lb])])

    st.subheader("Most Active Stocks - VALUE")
    sheet_name = "Sheet10"
    link = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name)
    actv = pd.read_csv(link)
    actvdf = pd.DataFrame(actv)
    actvdf.drop(actvdf.iloc[:, 1:5], inplace=True, axis=1)
    st.dataframe(actvdf)

    st.subheader("Most Active Stocks - VOLUME")
    sheet_name = "Sheet11"
    link = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name)
    actv1 = pd.read_csv(link)
    actvdf1 = pd.DataFrame(actv1)
    actvdf1.drop(actvdf1.iloc[:, 1:5], inplace=True, axis=1)
    st.dataframe(actvdf1)
  
    def generate_date_string():
        now = datetime.datetime.now()
        if now.weekday() == 5:
             date = now - datetime.timedelta(days=1)
        elif now.weekday() == 6:
             date = now - datetime.timedelta(days=2)
        else:
             if now.hour >= 18 and now.minute >= 30:
                    date = now
             else:
                  date = now - datetime.timedelta(days=1)
        date_string = date.strftime('%d%m%Y')
        return date_string
    date_variable = generate_date_string()
    url =f"https://archives.nseindia.com/products/content/sec_bhavdata_full_{date_variable}.csv"
    response = requests.get(url)
    c = pd.read_csv(StringIO(response.text))
    df = pd.DataFrame(c)
    df = df.drop([" TURNOVER_LACS", " NO_OF_TRADES", " DELIV_QTY", " OPEN_PRICE", " AVG_PRICE",
                      " TTL_TRD_QNTY"], axis=1)
    df['CHANGE'] = df.apply(lambda x: (x[' CLOSE_PRICE'] - x[' PREV_CLOSE']), axis=1)
    df['PCHANGE'] = df.apply(lambda x: (((x[' CLOSE_PRICE'] - x[' PREV_CLOSE']) / x[' CLOSE_PRICE']) * 100), axis=1)
    df['PCHANGE'] = df['PCHANGE'].apply(lambda x: round(x, 2))
    df=df.drop_duplicates(["SYMBOL"])

    indexnam=['NIFTYIT','NIFTYMEDIA','NIFTYREALTY','NIFTYPHARMA','NIFTYPSE','NIFTYMETAL', 'NIFTYAUTO', 'NIFTYFMCG', 'NIFTY50', "NIFTYNEXT50", "NIFTY100", "NIFTY200", "NIFTY500", "NIFTYSMALLCAP50", "NIFTYSMALLCAP100", "NIFTYSMALLCAP250", "NIFTYMIDCAP50", "NIFTYMIDCAP100", "NIFTYMIDCAP50"]
    opt=st.selectbox("select index", indexnam)
    indexnaml=opt.lower( )
    data = pd.read_csv(f"https://archives.nseindia.com/content/indices/ind_{indexnaml}list.csv")
    datadf = pd.DataFrame(data)
    list=(datadf['Symbol'].values.tolist())
    list1 = [symbol + ".NS" for symbol in list]
    df_week_highs_lows = pd.DataFrame(columns=['Ticker', '52_Week_High', '52_Week_Low'])
    for ticker in list1:
          # Fetch historical data from Yahoo Finance
          stock_data = yf.Ticker(ticker)
          historical_data = stock_data.history(period="1y")
          historical_data['1week_performance'] = historical_data['Close'].pct_change(periods=7) * 100
          historical_data['1week_performance']=historical_data['1week_performance'].round(4)
          historical_data['1month_performance'] = historical_data['Close'].pct_change(periods=21) * 100
          historical_data['3month_performance'] = historical_data['Close'].pct_change(periods=63) * 100
          historical_data['20-day SMA'] = historical_data['Close'].rolling(window=20).mean()
          historical_data['50-day SMA'] = historical_data['Close'].rolling(window=50).mean()
          historical_data['200-day SMA'] = historical_data['Close'].rolling(window=200).mean()
          fifty_two_week_high = historical_data['High'].max()
          fifty_two_week_low = historical_data['Low'].min()
          df_week_highs_lows = df_week_highs_lows._append(
           {'Ticker': ticker, '52_Week_High': fifty_two_week_high, '52_Week_Low': fifty_two_week_low}, ignore_index=True)
          
    df_week_highs_lows['Ticker'] = df_week_highs_lows['Ticker'].str.replace('.NS', '')
    df1=df[df['SYMBOL'].isin(list)]
    df2=df1[df1['SYMBOL'].isin(df_week_highs_lows['Ticker'])]
    df2= pd.merge(df2,df_week_highs_lows[["52_Week_High","52_Week_Low"]], on=df2['SYMBOL'], how='outer')
    df2=df2.drop("key_0",axis=1)
    df2['Distance_%HIGH'] = ((df2['52_Week_High'] - df2[' CLOSE_PRICE']) / df2['52_Week_High']) * 100
    total_stocks = len(df2)
    col1,col2=st.columns(2)
    with col1:
            def load_lottieurl_1(url: str):
                 r = requests.get(url)
                 if r.status_code != 200:
                        return None
                 return r.json()
            url = load_lottieurl_1("https://assets2.lottiefiles.com/private_files/lf30_1l8zkdv6.json")
            st_lottie(url, height=100)
            st.header(" Top gainers today!")
            st.dataframe(df2.sort_values(by=['PCHANGE'], ascending=False))#for top gainer
    with col2:
            def load_lottieurl_2(url: str):
                r = requests.get(url)
                if r.status_code != 200:
                           return None
                return r.json()
            url = load_lottieurl_2("https://assets8.lottiefiles.com/private_files/lf30_290nyta6.json")
            st_lottie(url, height=100)
            st.header("Top losers today!")
            st.dataframe(df2.sort_values(by=['PCHANGE'], ascending=True)) 
    list2=df2["SYMBOL"].values.tolist()
    list3 = [symbol + ".NS" for symbol in list2]
    st.caption("Stocks Near 52 Week High")
    filtered_stocks = df2[df2['Distance_%HIGH'] <= 7]
    num_filtered_stocks = len(filtered_stocks)
    percentage_near_52_week_high = (num_filtered_stocks / total_stocks) * 100 
    filtered_stock_names = filtered_stocks['SYMBOL'].tolist()
    st.write("**STOCKS** **NEAR** **52-WEEK** **HIGH**:", num_filtered_stocks)
    st.write("", filtered_stock_names)
    st.write("**%** **STOCKS** **NEAR** **52-WEEK** **HIGH**:",percentage_near_52_week_high)
    for tick in list3:
           with col1:
            intraday_data={}
            stock=yf.Ticker(tick)
            data=stock.history(interval="15m")
            intraday_data[tick]=data
            intraday_df=pd.concat(intraday_data.values(),keys=intraday_data.keys())
            fig = go.Figure(data=[go.Candlestick(x=[1,2,3,4,5,6,7,8,9,0,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40],
                                         open=intraday_df['Open'],
                                         high=intraday_df['High'],
                                         low=intraday_df['Low'],
                                         close=intraday_df['Close'])])
            fig.update_xaxes(rangeslider_visible=False)
            fig.update_layout(autosize=False, width=400, height=350, showlegend=False)
            fig.update_layout(title=f'{tick}',
                      xaxis_rangeslider_visible=False,
                      autosize=False,
                      width=400,
                      height=350,
                      showlegend=False)

            st.plotly_chart(fig)


    fig = plt.figure()
    fig.patch.set_facecolor('#121416')
    gs = fig.add_gridspec(9, 6)
    ax1 = fig.add_subplot(gs[0:4, 0:4])
    ax2 = fig.add_subplot(gs[0:2, 4:6])
    ax3 = fig.add_subplot(gs[2:4, 4:6])
    ax4 = fig.add_subplot(gs[4:6, 4:6])
    ax5 = fig.add_subplot(gs[4:6, 0:2])
    ax6 = fig.add_subplot(gs[4:6, 2:4])
    all_axes = fig.get_axes()
    for ax in fig.get_axes():
        ax.tick_params(bottom=False, labelbottom=False, left=False, labelleft=False)
    st.pyplot(fig)

if selected == "STOCK":
    tab1,tab2= st.tabs(["GENERAL INFO","FUNDAMENTAL"])
    with tab1:
        df = pd.read_csv('STOCKDATA.csv')
        dataa = st.selectbox('Which stock do you want to analyze?', df['Security Id'])
        df1 = pd.DataFrame(df)
        if len(dataa) > 0:
            option = []
            option.append(dataa)
        new_df = df[df1['Security Id'].isin(option)]
        col1, col2, col3 = st.columns(3)
        ddta = dataa+str(".NS")
        base = Ticker(ddta)

        col13,col14=st.columns(2)
        with col13:
            st.markdown( f"""<embed src="https://www.gateway-tt.in/trade?orderConfig=%5B%7B%22quantity%22%3A10%2C%22ticker%22%3A%22{dataa}%22%7D%5D&cardsize=big&withSearch=false&withTT=false" width="600" height="225">""",
            unsafe_allow_html=True)
        with col14:
            import streamlit.components.v1 as components
            components.html(f"""<blockquote class="trendlyne-widgets" data-get-url="https://trendlyne.com/web-widget/swot-widget/Poppins/{dataa}/?posCol=00A25B&primaryCol=006AFF&negCol=EB3B00&neuCol=F7941E" data-theme="light"></blockquote><script async src="https://cdn-static.trendlyne.com/static/js/webwidgets/tl-widgets.js" charset="utf-8"> </script>""",
            height=300)
        col6,col7=st.columns(2)
        with col6:
            start = st.date_input('start', value=pd.to_datetime('2022-08-03'))
            sdate=start.strftime("%Y-%m-%d")
        with col7:
            end = st.date_input('end', value=pd.to_datetime('today'))
            edate = end.strftime("%Y-%m-%d")
        if len(sdate)>0 and len(edate)>0:
            info4 = base.history(period="1d",start=sdate,end=edate,actions=False)
            df = pd.DataFrame(info4)
            df = df.reset_index(['Date'])
            df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            df['date']=pd.to_datetime(df['date'], unit='s')
            def pivotid(d_f_, l, n1, n2):
                if l-n1 < 0 or l+n2 >= len(d_f_):
                    return 0
                pividlow = 1
                pividhigh = 1
                for i in range(l-n1, l+n2+1):
                    if(d_f_.low[l] > d_f_.low[i]):
                        pividlow = 0
                    if(d_f_.high[l] < d_f_.high[i]):
                        pividhigh = 0

                if pividlow and pividhigh:
                    return 3
                elif pividlow:
                    return 1
                elif pividhigh:
                    return 2
                else:
                    return 0
            df['pivot']=df.apply(lambda x: pivotid(df, x.name, 5, 5), axis=1)
            def pointpos(x):
                if x['pivot']==1:
                    return x['low']-1e-3
                elif x['pivot']==2:
                    return x['high']+1e-3
                else:
                    return np.nan
            df['pointpos']=df.apply(lambda row: pointpos(row), axis=1)

            for i in range(2, df.shape[0]):
                current = df.iloc[i, :]
                prev = df.iloc[i - 1, :]
                prev_2 = df.iloc[i - 2, :]
                realbody = abs(current['open'] - current['close'])
                candle_range = current['high'] - current['low']
                idx = df.index[i]

                df.loc[idx, 'BULLISH PIN BAR'] = float(int(realbody <= candle_range / 3 and min(current['open'],
                                 current['close']) > (current['high'] + current['low']) / 2 and current['low'] < prev['low']))

                df.loc[idx, 'BEARISH PIN BAR'] = float(int(realbody <= candle_range / 3 and max(current['open'],
                        current['close']) < (current['high'] + current['low']) / 2 and current['high'] > prev['high']))

                df.loc[idx, 'INSIDE BAR'] = float(int(current['high'] < prev['high'] and current['low'] > prev['low']))

                df.loc[idx, 'BULLISH ENGULFING'] = float(int(current['high'] > prev['high'] and current['low'] <
                    prev['low'] and realbody >= 0.8 * candle_range and current['close'] > current['open']))

                df.loc[idx, 'BEARISH ENGULFING'] = float(int(current['high'] > prev['high'] and current['low'] <
                prev['low'] and realbody >= 0.8 * candle_range and current['close'] < current['open']))

                df.loc[idx, 'DOJI'] = float(int( candle_range <= 0.015 * current['open']))

            tab1, tab2, tab3 = st.tabs(["Chart", "Cndl Pattern", "Normalized"])
            with tab1:
                s = ['Candlestick', 'line']
                typpe = st.radio('Type of chart', s, horizontal=True)
                if typpe == 'Candlestick':
                    op1, op2, op3, op4, op5, op6, op7, op8=st.columns(8)
                    with op1:
                        button1=st.button("SMA")
                    with op2:
                        button2=st.button("BB")
                    with op3:
                        button3=st.button("PIVOT POINTS")
                    with op4:
                        button4=st.button("MACD")
                    with op5:
                        button5=st.button("RSI")
                    with op6:
                        button6=st.button("SUPERTREND")
                    with op7:
                        button7= st.button("ATR")
                    with op8:
                        button8=st.button("ADX")
                    fig=make_subplots(rows=3,cols=1)
                    fig.add_trace(go.Candlestick(x=df['date'],open=df['open'],high=df['high'],low=df['low'],close=df['close'],name='candle'))
                    fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "sun"])], rangeselector=dict(buttons=list([dict(count=1, label="1M", step="month", stepmode="backward"),dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"), dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1Y", step="year", stepmode="backward")])))
                    layout = go.Layout(plot_bgcolor='#efefef', font_family = 'Monospace', font_color = '#000000',
                                       font_size=20, xaxis=dict(rangeslider=dict(visible=False)))
                    fig.update_layout(layout)
                    fig.add_trace(go.Bar(x=df['date'], y=df['volume'], showlegend=False), row=2, col=1)
                    #fig.add_vline(x=, line_width=3, line_dash="dash", line_color="green",row=1,col=1
                    fig.update_layout(autosize=False, width=1050, height=1250, showlegend=False)
                    ROW=2
                    if button1:
                      df['MA1'] = ta.sma(df['close'], 20)
                      df['MA2'] = ta.sma(df['close'], 30)
                      df['MA3'] = ta.sma(df['close'], 40)
                      fig.add_scatter(x=df['date'], y=df['MA1'], name=f"{20}SMA")
                      fig.add_scatter(x=df['date'], y=df['MA2'], name=f"{30}SMA")
                      fig.add_scatter(x=df['date'], y=df['MA3'], name=f"{40}SMA")

                    if button2:
                       bb=ta.bbands(df['close'], length=20, std=2)
                       fig.add_trace(go.Scatter(x=df['date'], y=bb['BBU_20_2.0'], name='Upper Band', line=dict(color='#17becf', width=2)), row=1,col=1)
                       fig.add_trace(go.Scatter(x=df['date'], y=bb['BBL_20_2.0'], name='Lower Band', line=dict(color='#17becf', width=2)), row=1, col=1)
                       fig.add_trace(go.Scatter(x=df['date'], y=bb['BBM_20_2.0'], name='Middle Band', line=dict(color='#8c564b', width=2)), row=1, col=1)

                    if button3:
                        fig.add_scatter(x=df['date'], y=df['pointpos'], mode="markers",marker=dict(size=5, color="MediumPurple"), name="pivot")
                        fig.add_trace(go.Bar(x=df['date'], y=df['volume'], showlegend=False), row=2, col=1)

                    if button4:
                      macd=ta.macd(df['close'], fast=12, slow=26)
                      ROW=ROW+1
                      fig.add_trace((go.Scatter(x=df['date'], y=macd['MACD_12_26_9'], line=dict(color='#ff9900', width=2),
                                              name='macd', legendgroup='2')),row=ROW, col=1)

                      fig.add_trace(go.Scatter(x=df['date'], y=macd['MACDs_12_26_9'], line=dict(color='#000000', width=2),
                                             legendgroup='2', name='signal'),row=ROW, col=1)
                      colors = np.where(macd['MACDh_12_26_9'] < 0, '#000', '#ff9900')
                      fig.add_trace(go.Bar(x=df['date'], y=macd['MACDh_12_26_9'], name='histogram', marker_color=colors), row=ROW, col=1)

                    if button5:
                      df['RSI'] = ta.rsi(df['close'], 14)
                      ROW=ROW+1
                      fig.add_trace(go.Scatter(x=df['date'], y=df['RSI'], name='RSI', mode='lines+markers'), row=ROW, col=1)
                      fig.add_hline(y=30,line_dash="dot", row=ROW, col=1)
                      fig.add_hline(y=70, line_dash="dot", row=ROW, col=1)
                      plt.axhline(y=70, color='red', linestyle='-')

                    if button6:
                     sutdf=ta.supertrend(df['high'], df['low'], df['close'], 7, 3)
                     fig.add_trace(go.Scatter(x=df['date'], y=sutdf['SUPERT_7_3.0'], name='signal',
                                             line=dict(color='#17becf', width=2)), row=1, col=1)
                    if button7:
                       atr=ta.atr(df['high'], df['low'], df['close'], length=14)
                       ROW=ROW+1
                       fig.add_trace(go.Scatter(x=df['date'], y=atr, name='ATR'), row=ROW, col=1)

                    if button8:
                        adx=ta.adx(df['high'], df['low'], df['close'])
                        st.dataframe(adx)
                        ROW=ROW+1
                        fig.add_trace(go.Scatter(x=df['date'], y=adx['ADX_14'], name='ADX'), row=ROW, col=1)
                        fig.add_trace(go.Scatter(x=df['date'], y=adx['DMP_14'], name='+DMI'), row=ROW, col=1)
                        fig.add_trace(go.Scatter(x=df['date'], y=adx['DMN_14'], name='-DMI'), row=ROW, col=1)
                    st.plotly_chart(fig)

                else:
                    fig_ind=px.line(df['close'])
                    st.plotly_chart(fig_ind)

            with tab2:
                op=st.selectbox("select the chart pattern", ['BULLISH PIN BAR', 'BEARISH PIN BAR', 'INSIDE BAR', 'BULLISH ENGULFING', 'BEARISH ENGULFING', 'DOJI'])
                df.index = pd.DatetimeIndex(df['date'])
                candle = np.where(df[f'{op}'].tail(50) == 1, (0.97 * df.tail(50).low), np.nan)
                p = mpf.make_addplot(candle, type='scatter', marker='^', markersize=100)
                fig1 = mpf.plot(df.tail(50), type='candle', addplot= p)
                st.set_option('deprecation.showPyplotGlobalUse', False)
                st.pyplot(fig1)     
   
            from datetime import date

            start_date = "01-01-2023"
            today = date.today()
            end_date = today.strftime("%d-%m-%Y")

            from langchain.chains import LLMChain
            from langchain.prompts import PromptTemplate
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            from langchain_community.vectorstores.faiss import FAISS
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain_google_genai import ChatGoogleGenerativeAI
            from pypdf import PdfReader
            def parse_pdf(file):
                pdf = PdfReader(file)
                output = []
                for page in pdf.pages:
                   text = page.extract_text()
                   output.append(text)
                return output

            uploaded_file = st.file_uploader("Upload a pdf, docx, or txt file",type=["pdf", "docx", "txt"], help="Scanned documents are not supported yet! ")
            if uploaded_file is not None:
                if uploaded_file.name.endswith(".pdf"):
                     doc=parse_pdf(uploaded_file)
                     llm=ChatGoogleGenerativeAI(model="gemini-pro", verbose=True, temperature=0.1, google_api_key="AIzaSyCmRpFgfYmqR1uzjNLOEuMXEis35ab8C7M")
                     if st.button("Summary"):
                         template = """Write a summary of the text delimited by triple backtick as a Financial Analyst
                         Return your response which covers the key points of the text in bullet points.
                           ```{text}```
                         BULLET POINT SUMMARY:"""
                         prompt = PromptTemplate(template=template, input_variables=["text"])
                         llm_chain = LLMChain(prompt=prompt, llm=llm)
                         summ=(llm_chain.invoke(doc))
                         st.write(summ['text'])           

if selected == "DEALS":
    tab7, tab8, tab9, tab12= st.tabs(['BULK', 'BLOCK', 'INSIDER', 'SHORT SELLING'])
    with tab7:
      sheet_id = "1T79XwzC8sG7pMHaNXYug9BJ9uwseBtLbrLM0G4seBAc"
      sheet_name = "Sheet3"
      link = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name)
      LARGEdealdf = pd.read_csv(link)
      LARGEdealdf.drop(['remarks'], inplace=True, axis=1)
      st.dataframe(LARGEdealdf)
    with tab8:
        sheet_id = "1T79XwzC8sG7pMHaNXYug9BJ9uwseBtLbrLM0G4seBAc"
        sheet_name = "Sheet2"
        link = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name)
        BULKdealdf = pd.read_csv(link)  
        BULKdealdf.drop(["change","pchange","lastPrice","previousClose"], inplace=True,axis=1)
        if len(BULKdealdf)==0:
            st.write("NO BULK DEAL FOUND")
        else:
            st.dataframe(BULKdealdf)

    with tab9:
        sheet_id = "1T79XwzC8sG7pMHaNXYug9BJ9uwseBtLbrLM0G4seBAc"
        sheet_name = "Sheet6"
        link = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name)
        insiderdf = pd.read_csv(link)  
        insiderdf.drop(["anex","tkdAcqm","buyValue","sellValue","buyQuantity","remarks","exchange","derivativeType","acqfromDt","acqtoDt","xbrl","tdpDerivativeContractType","pid"], axis=1, inplace=True)
        #person = ["Promoters", "Promoter", "Promoter Group"]
        #s = s[s["MODE OF ACQUISITION \n"] == 'Market Purchase']
        #s = s[s["CATEGORY OF PERSON \n"].isin(person)]
        st.dataframe(insiderdf)

    with tab12:
        st.write("https://www.nseindia.com/api/historical/short-selling")
      

if selected == "EVENT CALENDER":
    tab1, tab6, tab10= st.tabs(["CORPORATE ACTION", "EARNINGS", "EVENTS"])
    with tab1:
        sheet_id = "1T79XwzC8sG7pMHaNXYug9BJ9uwseBtLbrLM0G4seBAc"
        sheet_name = "Sheet5"
        link = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name)
        p = pd.read_csv(link) 
        para = st.selectbox('PURPOSE', p['purpose'].unique())
        option = []
        option.append(para)

        if len(para) > 0:
            new_df = p[p['purpose'].isin(option)]
            st.dataframe(new_df)
    with tab6:
        option1=['Financial Results', 'Financial Results/Dividend', 'Financial Results/Dividend/Other business matters', 'Financial Results/Dividend/Fund Raising']
        new_df1 = p[p['purpose'].isin(option1)]
        new_df1.drop(['bm_desc'], inplace=True, axis=1)
        #st.table(new_df1)

        if 'start' not in st.session_state:
            st.session_state.start = 0
        def display_rows(dataframe, start, end):
            st.table(dataframe.iloc[start:end])

        col44, col56, col67, col77, col88, col91= st.columns(6)
        display_rows(new_df1, st.session_state.start, st.session_state.start + 20)
        if st.session_state.start > 0:
            with col67:
                if st.button("Previous"):
                    st.session_state.start -= 20
        with col77:
            if st.button("Next"):
                st.session_state.start += 20

    with tab10:
        sheet_id = "1T79XwzC8sG7pMHaNXYug9BJ9uwseBtLbrLM0G4seBAc"
        sheet_name = "Sheet1"
        link = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name)
        data = pd.read_csv(link)
        data=data[data['series']=='EQ']
        data.drop(data.iloc[:, 7:10], inplace=True, axis=1)
        data.drop(data.iloc[:, 8:11], inplace=True, axis=1)
        data.drop(data.iloc[:, 1:4], inplace=True, axis=1)
        st.dataframe(data)

if selected == 'NEWS':
      Api_key ="d97a80e245b54857936a5036aa600775"
      url="https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=d97a80e245b54857936a5036aa600775"
      r=requests.get(url).json()
      artic= r['articles']
      for article in artic:
          st.header(article['title'])
          st.write("Published at:", article['publishedAt'])
          if article['author']:
              st.write("Author:", article['author'])
          st.write("Source:", article['source']['name'])
          st.write(article['url'])


    


