import requests
import streamlit
import pandas as pd
header = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/111.0.0.0 Safari/537.36",
    "Sec-Fetch-User": "?1", "Accept": "*/*", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate",
    "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9,hi;q=0.8"
    }

url="https://www.nseindia.com/api/historical/bulk-deals?from=18-12-2023&to=19-12-2023&csv=true"

def nse_urlfetch(url):
    r_session = requests.session()
    nse_live = r_session.get("http://nseindia.com", headers=header)
    return r_session.get(url, headers=header)

data_text = nse_urlfetch(url).text
with open('BLUK.csv', 'w') as f:
        f.write(data_text)
        f.close()
streamlit.dataframe= pd.read_csv('BULK.csv')
