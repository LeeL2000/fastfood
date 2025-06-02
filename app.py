import streamlit as st
import pandas as pd

# קריאת הקובץ (חשוב שהקובץ יהיה באותה תיקייה עם הקוד וששם הקובץ נכון)
df = pd.read_csv("FastFoodNutritionMenuV2.csv")

# כותרת האפליקציה
st.title("🧃 Fast Food Nutrition Viewer")

# הצגת תצוגה מקדימה של הנתונים
st.subheader("🔍 תצוגה מקדימה של הנתונים")
st.dataframe(df)

# בדיקה אם העמודה 'Company' קיימת לפני שימוש
if 'Company' in df.columns:
    # סינון לפי חברה
    companies = df['Company'].unique()
    selected_company = st.selectbox("בחרי חברה:", companies)

    # סינון הטבלה לפי החברה שנבחרה
    filtered_df = df[df['Company'] == selected_company]

    st.subheader(f"📊 פרטי תזונה של {selected_company}")
    st.dataframe(filtered_df)
else:
    st.warning("עמודת 'Company' לא נמצאה בנתונים.")
