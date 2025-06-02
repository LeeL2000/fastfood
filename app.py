import streamlit as st
import pandas as pd

# טוען את הנתונים בהתאם לבחירה
@st.cache_data
def load_data(version='V2'):
    file_path = f"FastFoodNutritionMenu{version}.csv"
    df = pd.read_csv(file_path)

    # ניקוי שמות עמודות
    df.columns = df.columns.str.strip()

    # המרה לעמודות מספריות
    numeric_cols = ['Calories', 'Calories from Fat', 'Total Fat (g)', 'Saturated Fat (g)', 'Trans Fat (g)',
                    'Cholesterol (mg)', 'Sodium (mg)', 'Carbs (g)', 'Fiber (g)', 'Sugars (g)', 'Protein (g)',
                    'Weight Watchers Pnts']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# כותרת
st.title("🍔 ניתוח תפריטי מזון מהיר")

# בחירת גרסה
version = st.selectbox("בחרי גרסה", options=["V2", "V3"])

# טעינת הדאטהסט
df = load_data(version)

# אם קיימת עמודת Company – נמשיך
if 'Company' in df.columns:
    company = st.selectbox("בחרי חברה", sorted(df['Company'].dropna().unique()))
    filtered = df[df['Company'] == company]

    st.subheader(f"📋 פריטים של {company}")
    st.dataframe(filtered[['Item', 'Calories', 'Total Fat (g)', 'Sodium (mg)', 'Protein (g)', 'Carbs (g)']])

    st.subheader("📊 ממוצעים תזונתיים")
    st.write(filtered.describe()[['Calories', 'Total Fat (g)', 'Sodium (mg)', 'Protein (g)', 'Carbs (g)']])

    st.subheader("🔥 פריטים עתירי קלוריות")
    top = filtered[['Item', 'Calories']].dropna().sort_values('Calories', ascending=False).head(10)
    st.bar_chart(top.set_index('Item'))

else:
    st.warning("⚠️ לא נמצאה עמודת Company — ודאי שאת טוענת את הקובץ הנכון.")
