import streamlit as st
import pandas as pd

url = "https://drive.google.com/uc?id=1JdmDIqq-2ypiP6VyzP3j4N2lglv8yjkg&export=download"
df = pd.read_csv(url)

st.title("🧃 Fast Food Nutrition Viewer")
st.subheader("🔍 תצוגה מקדימה של הנתונים")
st.dataframe(df)

if 'Company' in df.columns:
    companies = df['Company'].unique()
    selected_company = st.selectbox("בחרי חברה:", companies)
    filtered_df = df[df['Company'] == selected_company]
    st.subheader(f"📊 פרטי תזונה של {selected_company}")
    st.dataframe(filtered_df)
else:
    st.warning("עמודת 'Company' לא נמצאה בנתונים.")
