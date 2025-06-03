import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page config ---
st.set_page_config(page_title="Fast Food Nutrition Dashboard", layout="wide")

# --- Header ---
st.title("🍔 Fast Food Nutrition Analysis")
st.markdown("""
This interactive app presents nutritional insights from a combined fast food dataset.
Explore calories, fat, protein, sodium, and vitamin correlations through visualizations.
""")

# --- Load data ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/leel2000/fastfood/main/FOOD-DATA-COMBINED.csv"
    df = pd.read_csv(url)
    df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col])
    return df

full_df = load_data()

# --- Prepare Data ---
numeric_cols = full_df.select_dtypes(include=['float64', 'int64']).columns

# Optional calculated column
if 'Calories fromFat' in full_df.columns and 'Caloric Value' in full_df.columns:
    full_df['FatCaloriesPercentage'] = (full_df['Calories fromFat'] / full_df['Caloric Value']) * 100

# --- Section selector ---
section = st.selectbox("Choose a visualization:", (
    "1. Average Calories, Sodium and Fat",
    "2. Protein Distribution",
    "3. Average Calories by Food Type",
    "4. Fat Calorie Percentage by Source",
    "5. Nutrient Correlation Heatmap"
))

# --- Visualizations ---
if section.startswith("1"):
    st.header("1. Average Calories, Sodium and Fat")
    fig, ax = plt.subplots(figsize=(8, 4))
    full_df[['Caloric Value', 'Sodium', 'Fat']].mean().plot(kind='barh', ax=ax, color=['#9ecae1', '#fdd0a2', '#fdae6b'])
    ax.set_title("Average Values of Calories, Sodium and Fat", fontsize=14)
    ax.set_xlabel("Amount")
    st.pyplot(fig)

elif section.startswith("2"):
    st.header("2. Protein Distribution")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(full_df['Protein'], bins=30, kde=True, color="#a1d99b", ax=ax)
    ax.set_title("Distribution of Protein Values", fontsize=14)
    ax.set_xlabel("Protein (g)")
    st.pyplot(fig)

elif section.startswith("3"):
    st.header("3. Average Calories by Food")
    avg_cal = full_df.groupby('food')['Caloric Value'].mean().sort_values(ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(10, 5))
    avg_cal.plot(kind='bar', color='#c6dbef', ax=ax)
    ax.set_ylabel("Average Calories")
    ax.set_title("Top 15 Foods by Average Caloric Value")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

elif section.startswith("4") and 'FatCaloriesPercentage' in full_df.columns:
    st.header("4. Fat Calories Percentage by Source")
    avg_pct = full_df.groupby('Source File')['FatCaloriesPercentage'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    avg_pct.plot(kind='barh', color='#ffcc99', ax=ax)
    ax.set_title("Average Fat-Calorie % by Source")
    st.pyplot(fig)

elif section.startswith("5"):
    st.header("5. Nutrient Correlation Heatmap")
    corr = full_df[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, cmap='coolwarm', annot=False, linewidths=0.5, ax=ax)
    ax.set_title("Correlation Between Nutritional Variables", fontsize=14)
    st.pyplot(fig)

# --- Footer ---
st.markdown("---")
st.markdown("Developed by Lee Lior · Reichman University · 2025")

st.markdown("Developed by Lee Lior · Reichman University · 2025")
