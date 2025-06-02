import streamlit as st
import pandas as pd

url = "https://raw.githubusercontent.com/LeeL2000/fastfood/main/FastFoodNutritionMenuV2.csv"

try:
    df = pd.read_csv(url, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(url, encoding='latin1')

st.title("🧃 Fast Food Nutrition Viewer")

st.subheader("🔍 תצוגה מקדימה של הנתונים")
st.dataframe(df)

companies = df['Company'].unique()
selected_company = st.selectbox("בחרי חברה:", companies)
filtered_df = df[df['Company'] == selected_company]

st.subheader(f"📊 פרטי תזונה של {selected_company}")
st.dataframe(filtered_df)
