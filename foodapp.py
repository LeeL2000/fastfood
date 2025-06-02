import streamlit as st
import pandas as pd

try:
    df = pd.read_csv("FastFoodNutritionMenuV2.csv", encoding='utf-8')  # או 'latin1'
except Exception as e:
    st.error(f"שגיאה בטעינת הקובץ: {e}")
    st.stop()

st.title("🧃 Fast Food Nutrition Viewer")

st.subheader("🔍 תצוגה מקדימה של הנתונים")
st.dataframe(df)

if 'Company' not in df.columns:
    st.error("העמודה 'Company' לא נמצאה בקובץ הנתונים.")
    st.stop()

companies = df['Company'].unique()
selected_company = st.selectbox("בחרי חברה:", companies)
filtered_df = df[df['Company'] == selected_company]

st.subheader(f"📊 פרטי תזונה של {selected_company}")
st.dataframe(filtered_df)
