import streamlit as st
import requests

# FastAPI endpoint URL
fastapi_url = "http://127.0.0.1:5000/get_bulk_data"

# Make a request to the FastAPI endpoint
response = requests.get(fastapi_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response from FastAPI
    data = response.json()
    st.json(data)
