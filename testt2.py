import sqlite3
import pandas as pd
import streamlit as st
conn = sqlite3.connect('example.db')

# Create a cursor object
cursor = conn.cursor()

# Execute a SQL query
cursor.execute('SELECT * FROM fii_table')

# Fetch all the results
results = cursor.fetchall()

# Close the cursor and the connection
cursor.close()
conn.close()

# Create a pandas DataFrame from the results
df = pd.DataFrame(results)

# Print the DataFrame
st.dataframe(df)
