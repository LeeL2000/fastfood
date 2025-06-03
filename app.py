import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import numpy as np
import base64

# --- Page config ---
st.set_page_config(page_title="Fast Food Nutrition Dashboard", layout="wide", page_icon="🍔")

# --- Custom CSS for enhanced styling and effects ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #f5f7fa, #c3cfe2);
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp {
        background: linear-gradient(to right, #fdfbfb, #ebedee);
        padding: 20px;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #2c3e50;
    }
    .block-container {
        padding-top: 2rem;
    }
    .card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
        transition: transform 0.2s ease-in-out;
    }
    .card:hover {
        transform: scale(1.01);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .css-1d391kg, .stSidebar {
        background-color: #f0f2f6 !important;
    }
    .download-button {
        background-color: #ffcc99;
        color: black;
        border-radius: 5px;
        padding: 6px 10px;
        text-decoration: none;
        font-weight: bold;
    }
    .download-button:hover {
        background-color: #ffb366;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1046/1046784.png", width=80)
st.sidebar.title("🍴 Navigation")
st.sidebar.markdown("Welcome to the Fast Food Nutrition Explorer! Use filters below to explore the data.")

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

# --- Sidebar Filters ---
st.sidebar.subheader("🔍 Filter Items")

cal_min, cal_max = int(full_df['Caloric Value'].min()), int(full_df['Caloric Value'].max())
calories_range = st.sidebar.slider("Calories Range", min_value=cal_min, max_value=cal_max, value=(cal_min, cal_max))

prot_min, prot_max = int(full_df['Protein'].min()), int(full_df['Protein'].max())
protein_range = st.sidebar.slider("Protein Range (g)", min_value=prot_min, max_value=prot_max, value=(prot_min, prot_max))

search_text = st.sidebar.text_input("Search for Food (e.g. burger, salad)", "")

filtered_df = full_df[(full_df['Caloric Value'] >= calories_range[0]) &
                      (full_df['Caloric Value'] <= calories_range[1]) &
                      (full_df['Protein'] >= protein_range[0]) &
                      (full_df['Protein'] <= protein_range[1])]

if search_text:
    filtered_df = filtered_df[filtered_df['food'].str.contains(search_text, case=False, na=False)]

# --- Main Header ---
st.title("🍔 Fast Food Nutrition Dashboard")
st.markdown("""
Explore fast food nutritional data like never before! Use the filters on the left to search and narrow down menu items, visualize nutritional trends, and get smart recommendations.
""")

# --- Download filtered CSV ---
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # convert to base64
    href = f'<a href="data:file/csv;base64,{b64}" download="filtered_nutrition.csv" class="download-button">📥 Download Filtered Data</a>'
    return href

st.markdown(get_table_download_link(filtered_df), unsafe_allow_html=True)

# --- Tabs ---
tabs = st.tabs([
    "📋 Overview",
    "📈 Visual Insights",
    "📊 Nutrient Analysis",
    "🥇 Recommendations",
    "🧪 Correlation"
])

with tabs[0]:
    st.subheader("📋 Filtered Data Preview")
    st.dataframe(filtered_df.head(20))

with tabs[1]:
    st.subheader("📈 Average Calories, Sodium and Fat")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    filtered_df[['Caloric Value', 'Sodium', 'Fat']].mean().plot(kind='barh', ax=ax1, color=['#9ecae1', '#fdd0a2', '#fdae6b'])
    ax1.set_title("Average Nutrients")
    ax1.set_xlabel("Amount")
    st.pyplot(fig1)

    st.subheader("🍗 Protein Distribution")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.histplot(filtered_df['Protein'], bins=30, kde=True, color="#a1d99b", ax=ax2)
    ax2.set_title("Distribution of Protein Values")
    ax2.set_xlabel("Protein (g)")
    st.pyplot(fig2)

with tabs[2]:
    st.subheader("🥗 Average Calories by Food")
    avg_cal = filtered_df.groupby('food')['Caloric Value'].mean().sort_values(ascending=False).head(15)
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    avg_cal.plot(kind='bar', color='#c6dbef', ax=ax3)
    ax3.set_ylabel("Average Calories")
    ax3.set_title("Top 15 Foods by Average Caloric Value")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig3)

    st.subheader("🔥 Fat Calories Percentage by Source")
    if 'FatCaloriesPercentage' in filtered_df.columns and 'Source File' in filtered_df.columns:
        avg_pct = filtered_df.groupby('Source File')['FatCaloriesPercentage'].mean().sort_values()
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        avg_pct.plot(kind='barh', color='#ffcc99', ax=ax4)
        ax4.set_title("Fat-Calorie % by Source")
        st.pyplot(fig4)

with tabs[3]:
    st.subheader("🥇 Top Picks (High Protein / Low Fat)")
    top_items = filtered_df.sort_values(by=['Protein'], ascending=False)
    top_items = top_items[top_items['Fat'] < 20]
    top_items = top_items[['food', 'Caloric Value', 'Fat', 'Protein']].head(5)

    for idx, row in top_items.iterrows():
        st.markdown(f"""
        <div class="card">
        <strong>{row['food']}</strong><br>
        Calories: {row['Caloric Value']} | Protein: {row['Protein']}g | Fat: {row['Fat']}g
        </div>
        """, unsafe_allow_html=True)

with tabs[4]:
    st.subheader("🧪 Nutrient Correlation Heatmap")
    corr = filtered_df[numeric_cols].corr()
    fig5, ax5 = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, cmap='coolwarm', annot=True, fmt=".2f", linewidths=0.5, ax=ax5)
    ax5.set_title("Correlation Between Nutritional Variables")
    st.pyplot(fig5)

# --- Footer ---
st.markdown("---")
st.markdown("Developed by **Lee Lior** · Reichman University · 2025 | Designed with ❤️ using Streamlit")
