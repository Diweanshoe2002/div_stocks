import redis
import streamlit as st
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

C=r.get("INDEXDATA")
st.json(C)
