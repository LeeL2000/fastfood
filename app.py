import streamlit as st
import pandas as pd

# קריאת הקובץ (חשוב שהשם יהיה בדיוק כך ושיהיה באותה תיקייה!)
df = pd.read_csv("FastFoodNutritionMenuV2.csv")

# כותרת
st.title("🧃 Fast Food Nutrition Viewer")

# הצגת הטבלה
st.subheader("🔍 תצוגה מקדימה של הנתונים")
st.dataframe(df)

# סינון לפי חברה
companies = df['Company'].unique()
selected_company = st.selectbox("בחרי חברה:", companies)
filtered_df = df[df['Company'] == selected_company]

st.subheader(f"📊 פרטי תזונה של {selected_company}")
st.dataframe(filtered_df)
