import streamlit as st
import pandas as pd

# פונקציה לטעינת הדאטה מגוגל דרייב (דרך שיתוף קובץ)
@st.cache_data
def load_data():
    url = 'https://drive.google.com/uc?id=1cPe6NLZP1iO2Cse-8yIVdRzrdAvaqhHo'
    df = pd.read_csv(url, encoding='latin1')
    df.columns = df.columns.str.replace('\n', '').str.strip()
    
    # המרה למספרים וטיוב נתונים
    numeric_cols = ['Calories', 'Calories fromFat', 'Total Fat(g)', 'Saturated Fat(g)', 'Trans Fat(g)',
                    'Cholesterol(mg)', 'Sodium (mg)', 'Carbs(g)', 'Fiber(g)', 'Sugars(g)', 'Protein(g)',
                    'Weight WatchersPnts']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# טעינת הנתונים
df = load_data()

st.title("ניתוח תפריטי מזון מהיר")
st.markdown("נתונים מתוך תפריטי חברות מזון מהיר. ניתן לסנן לפי חברה ולבחון ערכים תזונתיים.")

# סינון לפי חברה
companies = df['Company'].dropna().unique()
selected_company = st.selectbox("בחרי חברה", sorted(companies))

filtered_df = df[df['Company'] == selected_company]

# הצגת טבלה
st.subheader(f"פרטי פריטים של {selected_company}")
st.dataframe(filtered_df[['Item', 'Calories', 'Total Fat(g)', 'Sodium (mg)', 'Protein(g)', 'Carbs(g)']])

# ממוצעים
st.subheader("ממוצעים תזונתיים לפריטים שנבחרו:")
st.write(filtered_df.describe().loc['mean'][['Calories', 'Total Fat(g)', 'Sodium (mg)', 'Protein(g)', 'Carbs(g)']])

# גרף
st.subheader("השוואת קלוריות לפריטים שונים")
top_items = filtered_df[['Item', 'Calories']].dropna().sort_values('Calories', ascending=False).head(10)
st.bar_chart(top_items.set_index('Item'))
