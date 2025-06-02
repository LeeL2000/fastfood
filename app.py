import streamlit as st
import pandas as pd

# טוען את הנתונים בהתאם לבחירת הגרסה
@st.cache_data
def load_data(version='V2'):
    file_path = f"FastFoodNutritionMenu{version}.csv"
    df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')

    # ניקוי עמודות
    df.columns = df.columns.str.replace('\n', '').str.strip()

    # המרה לעמודות מספריות
    numeric_cols = ['Calories', 'Calories fromFat', 'Total Fat(g)', 'Saturated Fat(g)', 'Trans Fat(g)',
                    'Cholesterol(mg)', 'Sodium (mg)', 'Carbs(g)', 'Fiber(g)', 'Sugars(g)', 'Protein(g)',
                    'Weight WatchersPnts']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# כותרת האפליקציה
st.title("🍔 ניתוח תזונתי של תפריטי מזון מהיר")

# בחירת גרסת הדאטה
version = st.selectbox("בחרי גרסת דאטה", options=["V2", "V3"])

# טעינת הדאטה המתאימה
df = load_data(version)

# בדיקה אם קיימת עמודת Company
if 'Company' in df.columns:
    companies = sorted(df['Company'].dropna().unique())
    selected_company = st.selectbox("בחרי חברה", companies)

    filtered_df = df[df['Company'] == selected_company]

    st.subheader(f"📋 פריטי תפריט של {selected_company}")
    st.dataframe(filtered_df[['Item', 'Calories', 'Total Fat(g)', 'Sodium (mg)', 'Protein(g)', 'Carbs(g)']])

    st.subheader("📊 ממוצעים תזונתיים לפריטים שנבחרו")
    st.write(filtered_df.describe()[['Calories', 'Total Fat(g)', 'Sodium (mg)', 'Protein(g)', 'Carbs(g)']])

    st.subheader("🔥 פריטים עם הכי הרבה קלוריות")
    top_items = filtered_df[['Item', 'Calories']].dropna().sort_values('Calories', ascending=False).head(10)
    st.bar_chart(top_items.set_index('Item'))

else:
    st.warning("⚠️ לא נמצאה עמודה בשם 'Company'. ודאי שהקובץ נכון.")
