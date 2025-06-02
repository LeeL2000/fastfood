import streamlit as st
import pandas as pd

# הקישור להורדה ישירה מהקובץ שלך בגוגל דרייב
url = "https://drive.google.com/uc?export=download&id=1cPe6NLZP1iO2Cse-8yIVdRzrdAvaqhHo"

try:
    df = pd.read_csv(url, encoding='utf-8-sig', on_bad_lines='skip')
except UnicodeDecodeError:
    df = pd.read_csv(url, encoding='latin1', on_bad_lines='skip')

st.title("🧃 Fast Food Nutrition Viewer")

st.subheader("🔍 תצוגה מקדימה של הנתונים")
st.dataframe(df)

companies = df['Company'].unique()
selected_company = st.selectbox("בחרי חברה:", companies)
filtered_df = df[df['Company'] == selected_company]

st.subheader(f"📊 פרטי תזונה של {selected_company}")
st.dataframe(filtered_df)
