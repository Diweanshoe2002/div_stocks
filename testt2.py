import gspread
import pandas as pd
import streamlit as st
sheet_id = "1T79XwzC8sG7pMHaNXYug9BJ9uwseBtLbrLM0G4seBAc"
sheet_name = "Sheet1"
sheet_name1="Sheet2"
link = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name)
df = pd.read_csv(link)
st.dataframe(df)
link1 = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(sheet_id, sheet_name1)
df1 = pd.DataFrame(link1)
st.dataframe(df1)
