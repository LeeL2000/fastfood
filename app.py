import streamlit as st
import pandas as pd

# פונקציה לטעינת הקובץ לפי גרסה
@st.cache_data
def load_data(version='V2'):
    file_path = f"FastFoodNutritionMenu{version}.csv"
    df = pd.read_csv(file_path)

    # ניקוי שמות עמודות
    df.columns = df.columns.str.strip()

    # המרה לעמודות מספריות (מותאם לשמות מתוך הקובץ שלך)
    numeric_cols = ['Calories', 'Calories fromFat', 'Total Fat(g)', 'Saturated Fat(g)', 'Trans Fat(g)',
                    'Cholesterol(mg)', 'Sodium (mg)', 'Carbs(g)', 'Fiber(g)', 'Sugars(g)', 'Protein(g)',
                    'Weight WatchersPnts']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# כותרת האפליקציה
st.title("🍔 ניתוח תפריטי מזון מהיר")

# בחירת גרסה
version = st.selectbox("בחרי גרסת דאטה", options=["V2", "V3"])

# טוען את הדאטה
df = load_data(version)

# הצגת שמות העמודות לבדיקה (לא חובה - רק לניפוי תקלות)
# st.write("🧾 שמות העמודות בדאטה:", df.columns.tolist())

# בדיקה אם קיימת עמודת Company
if 'Company' in df.columns:
    company = st.selectbox("בחרי חברה", sorted(df['Company'].dropna().unique()))
    filtered = df[df['Company'] == company]

    st.subheader(f"📋 פריטים מתוך {company}")
    columns_to_show = ['Item', 'Calories', 'Total Fat(g)', 'Sodium (mg)', 'Protein(g)', 'Carbs(g)']
    existing_columns = [col for col in columns_to_show if col in filtered.columns]
    st.dataframe(filtered[existing_columns])

    st.subheader("📊 ממוצעים תזונתיים")
    st.write(filtered.describe()[existing_columns])

    st.subheader("🔥 פריטים עם הכי הרבה קלוריות")
    if 'Calories' in filtered.columns and 'Item' in filtered.columns:
        top = filtered[['Item', 'Calories']].dropna().sort_values('Calories', ascending=False).head(10)
        st.bar_chart(top.set_index('Item'))
    else:
        st.warning("אין עמודות 'Item' או 'Calories' להצגה בגרף.")
else:
    st.warning("⚠️ לא נמצאה עמודת Company בקובץ הנתונים.")
