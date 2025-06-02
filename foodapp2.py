import streamlit as st
import pandas as pd
import requests
from io import StringIO

url = "https://drive.google.com/uc?export=download&id=1cPe6NLZP1iO2Cse-8yIVdRzrdAvaqhHo"

response = requests.get(url)
response.encoding = 'utf-8'  # אפשר לשנות ל'latin1' אם צריך

try:
    data = StringIO(response.text)
    df = pd.read_csv(data)
except UnicodeDecodeError:
    response.encoding = 'latin1'
    data = StringIO(response.text)
    df = pd.read_csv(data)

st.title("🧃 Fast Food Nutrition Viewer")

st.subheader("🔍 תצוגה מקדימה של הנתונים")
st.dataframe(df)

companies = df['Company'].unique()
selected_company = st.selectbox("בחרי חברה:", companies)
filtered_df = df[df['Company'] == selected_company]

st.subheader(f"📊 פרטי תזונה של {selected_company}")
st.dataframe(filtered_df)
