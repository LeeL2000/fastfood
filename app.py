import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page config ---
st.set_page_config(page_title="Fast Food Nutrition Dashboard", layout="wide")

# --- Sidebar ---
st.sidebar.title("🍴 Navigation")
st.sidebar.markdown("Select the section you want to explore.")

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

if 'Calories fromFat' in full_df.columns and 'Caloric Value' in full_df.columns:
    full_df['FatCaloriesPercentage'] = (full_df['Calories fromFat'] / full_df['Caloric Value']) * 100

# --- Header ---
st.title("🍔 Fast Food Nutrition Dashboard")
st.markdown("""
Analyze and visualize nutritional information from various fast food items.
Use the tabs below to explore calories, protein, fat, sodium and correlations.
""")

# --- Tabs ---
tabs = st.tabs([
    "📊 Overview",
    "🍟 Avg Calories, Sodium, Fat",
    "🍗 Protein Distribution",
    "🥗 Avg Calories by Food",
    "🔥 Fat-Calorie % by Source",
    "🧪 Nutrient Correlation"
])

with tabs[0]:
    st.subheader("📋 Dataset Preview")
    st.dataframe(full_df.head())
    st.markdown("""
    This dataset includes a variety of fast food items and their detailed nutritional values, such as:
    - Calories
    - Fat (total, saturated, mono, poly)
    - Carbohydrates, Sugars, Protein
    - Vitamins and Minerals
    """)

with tabs[1]:
    st.subheader("🍟 Average Calories, Sodium and Fat")
    fig, ax = plt.subplots(figsize=(8, 4))
    full_df[['Caloric Value', 'Sodium', 'Fat']].mean().plot(kind='barh', ax=ax, color=['#9ecae1', '#fdd0a2', '#fdae6b'])
    ax.set_title("Average Values of Calories, Sodium and Fat", fontsize=14)
    ax.set_xlabel("Amount")
    st.pyplot(fig)

with tabs[2]:
    st.subheader("🍗 Protein Distribution")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(full_df['Protein'], bins=30, kde=True, color="#a1d99b", ax=ax)
    ax.set_title("Distribution of Protein Values", fontsize=14)
    ax.set_xlabel("Protein (g)")
    st.pyplot(fig)

with tabs[3]:
    st.subheader("🥗 Average Calories by Food")
    avg_cal = full_df.groupby('food')['Caloric Value'].mean().sort_values(ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(10, 5))
    avg_cal.plot(kind='bar', color='#c6dbef', ax=ax)
    ax.set_ylabel("Average Calories")
    ax.set_title("Top 15 Foods by Average Caloric Value")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

with tabs[4]:
    st.subheader("🔥 Fat Calories Percentage by Source")
    if 'FatCaloriesPercentage' in full_df.columns and 'Source File' in full_df.columns:
        avg_pct = full_df.groupby('Source File')['FatCaloriesPercentage'].mean().sort_values()
        fig, ax = plt.subplots(figsize=(8, 5))
        avg_pct.plot(kind='barh', color='#ffcc99', ax=ax)
        ax.set_title("Average Fat-Calorie % by Source")
        st.pyplot(fig)
    else:
        st.warning("Required columns not found in the dataset.")

with tabs[5]:
    st.subheader("🧪 Nutrient Correlation Heatmap")
    corr = full_df[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, cmap='coolwarm', annot=False, linewidths=0.5, ax=ax)
    ax.set_title("Correlation Between Nutritional Variables", fontsize=14)
    st.pyplot(fig)

# --- Footer ---
st.markdown("---")
st.markdown("Developed by Lee Lior · Reichman University · 2025")
