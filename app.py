import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# הקישור לקובץ בדרייב (בפורמט מתאים)
url = "https://drive.google.com/uc?export=download&id=1cPe6NLZP1iO2Cse-8yIVdRzrdAvaqhHo"

# ניסיון להוריד ולטעון את הקובץ
try:
    response = requests.get(url)
    df = pd.read_csv(BytesIO(response.content), encoding='latin1', on_bad_lines='skip', engine='python')
except Exception as e:
    st.error(f"❌ שגיאה בקריאת הקובץ: {e}")
    st.stop()

# כותרת
st.title("🧃 Fast Food Nutrition Viewer")

# הצגת טבלת הנתונים
st.subheader("🔍 תצוגה מקדימה של הנתונים")
st.dataframe(df)

# תיבת בחירה לפי חברה
if 'Company' in df.columns:
    companies = df['Company'].unique()
    selected_company = st.selectbox("בחרי חברה:", companies)

    filtered_df = df[df['Company'] == selected_company]
    st.subheader(f"📊 פרטי תזונה של {selected_company}")
    st.dataframe(filtered_df)
else:
    st.warning("לא נמצאה עמודת 'Company' בקובץ.")
