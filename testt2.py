import streamlit as st
import pandas as pd
import requests

def nse_headers_session(url):
    baseurl = "https://www.nseindia.com/"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                             'like Gecko) '
                             'Chrome/80.0.3987.149 Safari/537.36',
               'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
    session = requests.Session()
    request = session.get(baseurl, headers=headers)
    cookies = dict(request.cookies)
    response = session.get(url, headers=headers, cookies=cookies)
    raw = (response.json())
    return raw

j=nse_headers_session("https://www.nseindia.com/api/corporates-pit?index=equities&from_date=01-01-2022&to_date=30-12-2023&symbol=ETHOSLTD")
df=pd.DataFrame(j['data'])
st.dataframe(df)
