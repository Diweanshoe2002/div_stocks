from fastapi import FastAPI
import requests
app = FastAPI()

def nse_urlfetch(url):
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
    r_session = requests.session()
    nse_live = r_session.get("http://nseindia.com", headers=header)
    return r_session.get(url, headers=header)
@app.get("/fiidii_trade")
def get_fii_data():
    url = "https://www.nseindia.com/api/fiidiiTradeReact"
    data_text = nse_urlfetch(url).json()
    return data_text
@app.get("/indexdata")
def get_index_data():
    url = "https://www.nseindia.com/api/allIndices"
    data_text1 = nse_urlfetch(url).json()
    return data_text1


