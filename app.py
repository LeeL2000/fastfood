import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title and Intro
st.title("🍔 Fast Food Nutrition Analysis")
st.markdown("This interactive dashboard explores nutritional information across various fast food items. Insights include calories, fat, sodium, protein, and more.")

# Load unified dataset from GitHub
@st.cache_data

def load_data():
    url = "https://raw.githubusercontent.com/leel2000/fastfood/main/FOOD-DATA-COMBINED.csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()

    numeric_cols = ['Caloric Value', 'Fat', 'Saturated Fats', 'Carbohydrates',
                    'Sugars', 'Protein', 'Sodium']

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['FatCalories'] = df['Fat'] * 9
    df['FatCaloriesPercentage'] = (df['FatCalories'] / df['Caloric Value']) * 100
    df = df.dropna(subset=['Caloric Value', 'FatCaloriesPercentage'])
    return df

# Load and clean data
df = load_data()
st.dataframe(df.head())

# Graph 1: Average Calories, Sodium and Fat
st.subheader("1. Average Calories, Sodium and Fat")
fig1, ax1 = plt.subplots()
df[['Caloric Value', 'Sodium', 'Fat']].mean().sort_values().plot(kind='barh', ax=ax1, color=['#FF9999', '#FFCC99', '#99CCFF'])
ax1.set_title("Average Values of Calories, Sodium and Fat")
st.pyplot(fig1)

# Graph 2: Protein Distribution
st.subheader("2. Protein Distribution")
fig2, ax2 = plt.subplots()
sns.histplot(df['Protein'], bins=20, kde=True, ax=ax2, color='#66C2A5')
ax2.set_title("Distribution of Protein Values")
st.pyplot(fig2)

# Graph 3: Average Calories by Food Group
st.subheader("3. Average Calories by Food Group")
if 'Source File' in df.columns:
    fig3, ax3 = plt.subplots()
    df.groupby('Source File')['Caloric Value'].mean().sort_values().plot(kind='bar', ax=ax3, color='#8DA0CB')
    ax3.set_title("Average Calories by Food Source")
    st.pyplot(fig3)

# Graph 4: Fat Calories Percentage by Source
st.subheader("4. Fat Calories % by Source")
if 'Source File' in df.columns:
    fig4, ax4 = plt.subplots()
    df.groupby('Source File')['FatCaloriesPercentage'].mean().sort_values().plot(kind='barh', ax=ax4, color='#FC8D62')
    ax4.set_title("Avg % of Calories from Fat by Food Source")
    st.pyplot(fig4)

# Graph 5: Correlation Heatmap
st.subheader("5. Nutrient Correlation Heatmap")
numeric_df = df.select_dtypes(include=['float64', 'int64'])
fig5, ax5 = plt.subplots(figsize=(10, 8))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax5)
ax5.set_title("Correlation Between Nutritional Variables")
st.pyplot(fig5)

# Footer
st.markdown("---")
st.markdown("App created by Lee Lior · 2025 · Reichman University")
