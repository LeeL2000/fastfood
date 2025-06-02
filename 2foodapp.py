import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# הקישור להורדת הקובץ מגוגל דרייב
url = "https://drive.google.com/uc?export=download&id=1cPe6NLZP1iO2Cse-8yIVdRzrdAvaqhHo"

# בקשת הורדה
response = requests.get(url)

# קריאה באמצעות BytesIO כדי לטפל בקידוד
try:
    df = pd.read_csv(BytesIO(response.content), encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(BytesIO(response.content), encoding='latin1')

# כותרת האפליקציה
st.title("🧃 Fast Food Nutrition Viewer")

# הצגת טבלה כללית
st.subheader("🔍 תצוגה מקדימה של הנתונים")
st.dataframe(df)

# סינון לפי חברה
companies = df['Company'].unique()
selected_company = st.selectbox("בחרי חברה:", companies)
filtered_df = df[df['Company'] == selected_company]

# הצגת תוצאות הסינון
st.subheader(f"📊 פרטי תזונה של {selected_company}")
st.dataframe(filtered_df)

