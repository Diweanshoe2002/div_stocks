import gspread
import pandas as pd
import streamlit as st
gc = gspread.service_account(filename='service_account.json')
sheet_id = "1T79XwzC8sG7pMHaNXYug9BJ9uwseBtLbrLM0G4seBAc"
sheet_name = "Sheet1"
sheet_name1="Sheet2"
link = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name)
sh = gc.open_by_url(link)
ws = sh.worksheet(sheet_name)
df = pd.DataFrame(ws.get_all_records())
st.dataframe(df)
link1 = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name1)
sh1 = gc.open_by_url(link1)
ws1 = sh1.worksheet(sheet_name1)
df1 = pd.DataFrame(ws1.get_all_records())
st.dataframe(df1)
