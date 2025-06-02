import streamlit as st
import pandas as pd

# פונקציה לטעינת הנתונים לפי גרסה
@st.cache_data
def load_data(version='V2'):
    file_path = f"FastFoodNutritionMenu{version}.csv"
    df = pd.read_csv(file_path)

    # ניקוי שמות עמודות
    df.columns = df.columns.str.strip()

    # המרה לעמודות מספריות (בהתאם לשמות מהקובץ שלך)
    numeric_cols = ['Calories', 'Calories fromFat', 'Total Fat(g)', 'Saturated Fat(g)', 'Trans Fat(g)',
                    'Cholesterol(mg)', 'Sodium (mg)', 'Carbs(g)', 'Fiber(g)', 'Sugars(g)', 'Protein(g)',
                    'Weight WatchersPnts']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# כותרת האפליקציה
st.title("🍔 ניתוח תפריטי מזון מהיר")

# בחירת גרסת הדאטה
version = st.selectbox("בחרי גרסת דאטה", options=["V2", "V3"])

# טעינת הדאטהסט הנבחר
df = load_data(version)

# בדיקה אם קיימת עמודת Company
if 'Company' in df.columns:
    company = st.selectbox("בחרי חברה", sorted(df['Company'].dropna().unique()))
    filtered = df[df['Company'] == company]

    # הצגת טבלה של הפריטים
    st.subheader(f"📋 פריטים מתוך {company}")
    columns_to_show = ['Item', 'Calories', 'Total Fat(g)', 'Sodium (mg)', 'Protein(g)', 'Carbs(g)']
    existing_columns = [col for col in columns_to_show if col in filtered.columns]
    st.dataframe(filtered[existing_columns])

    # ממוצעים תזונתיים
    st.subheader("📊 ממוצעים תזונתיים")
    numeric_existing = filtered[existing_columns].select_dtypes(include='number').columns
    if not numeric_existing.empty:
        st.write(filtered.describe()[numeric_existing])
    else:
        st.info("אין עמודות מספריות זמינות להצגת ממוצעים.")

    # גרף קלוריות
    st.subheader("🔥 פריטים עם הכי הרבה קלוריות")
    if 'Calories' in filtered.columns and 'Item' in filtered.columns:
        top = filtered[['Item', 'Calories']].dropna().sort_values('Calories', ascending=False).head(10)
        st.bar_chart(top.set_index('Item'))
    else:
        st.warning("לא נמצאו עמודות 'Item' או 'Calories' להצגת גרף.")
else:
    st.warning("⚠️ לא נמצאה עמודת Company בקובץ הנתונים.")
