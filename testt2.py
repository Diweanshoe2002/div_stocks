import redis
import requests
import json
import streamlit as st
# Redis connection
r = redis.Redis(
    host='redis-11380.c239.us-east-1-2.ec2.redns.redis-cloud.com',
    port=11380,
    password='bwfZX0ImvrVqoD4uKh8gPfD2vIJSBTvx',
    decode_responses=True
)

# Test the Redis connection
try:
    r.ping()
    st.write("Connected to Redis successfully!")
except redis.ConnectionError:
    st.write("Failed to connect to Redis.")
    exit(1)

def nse_headers_session(url):
    baseurl = "https://www.nseindia.com/"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'accept-language': 'en,gu;q=0.9,hi;q=0.8',
        'accept-encoding': 'gzip, deflate, br'
    }
    session = requests.Session()
    request = session.get(baseurl, headers=headers)
    cookies = dict(request.cookies)
    response = session.get(url, headers=headers, cookies=cookies)
    raw = response.json()
    return raw


def fetch_and_store_nse_data(symbol="AXISBANK", corp_type="announcement", market="equities"):
    url = f"https://www.nseindia.com/api/corp-info?symbol={symbol}&corpType={corp_type}&market={market}"

    try:
        data = nse_headers_session(url)

        # Store the entire response as a JSON string
        key = f"nse:{symbol}:{corp_type}:{market}"
        r.set(key, json.dumps(data))
        print(f"Data stored in Redis with key: {key}")

        # Optionally, store individual announcements as separate keys
        if 'announcements' in data:
            for idx, announcement in enumerate(data['announcements']):
                announcement_key = f"{key}:announcement:{idx}"
                r.set(announcement_key, json.dumps(announcement))
                print(f"Stored announcement with key: {announcement_key}")

    except Exception as e:
        print(f"Error fetching or storing data: {e}")


# Fetch and store data
fetch_and_store_nse_data()

# Retrieve and print stored data (for verification)
stored_data = r.get("nse:AXISBANK:announcement:equities")
if stored_data:
    st.write("Retrieved data from Redis:")
    st.dataframe(stored_data)
else:
    print("No data found in Redis.")
