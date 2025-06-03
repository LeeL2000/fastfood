import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import numpy as np
import base64

# --- Page config ---
st.set_page_config(page_title="Fast Food Nutrition Dashboard", layout="wide", page_icon="🍔")

# --- Enhanced Styling CSS ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #fff5e6, #ffe0cc);
    }
    .stApp {
        background: #fffaf2;
        font-family: 'Segoe UI', sans-serif;
        padding: 20px;
    }
    .block-container {
        padding-top: 2rem;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #cc5200;
    }
    .card {
        background-color: #fff8f0;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        margin-bottom: 16px;
        transition: all 0.2s ease-in-out;
    }
    .card:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.25);
    }
    .stSidebar {
        background: #fff2e6;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 18px;
        font-weight: bold;
        color: #cc5200;
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
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1046/1046784.png", width=80)
st.sidebar.title("🍴 Navigation")
st.sidebar.markdown("Welcome to the Fast Food Nutrition Explorer!")

# --- Load Data ---
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/leel2000/fastfood/main/FOOD-DATA-COMBINED.csv"
    df = pd.read_csv(url)
    df = df.drop(columns=[col for col in df.columns if 'Unnamed' in col])
    return df

full_df = load_data()

# --- Clean & Prepare ---
numeric_cols = full_df.select_dtypes(include=['float64', 'int64']).columns
if 'Calories fromFat' in full_df.columns and 'Caloric Value' in full_df.columns:
    full_df['FatCaloriesPercentage'] = (full_df['Calories fromFat'] / full_df['Caloric Value']) * 100

# --- Sidebar Filters ---
cal_min, cal_max = int(full_df['Caloric Value'].min()), int(full_df['Caloric Value'].max())
prot_min, prot_max = int(full_df['Protein'].min()), int(full_df['Protein'].max())

st.sidebar.subheader("🔍 Filter Items")
calories_range = st.sidebar.slider("Calories Range", min_value=cal_min, max_value=cal_max, value=(cal_min, cal_max))
protein_range = st.sidebar.slider("Protein Range (g)", min_value=prot_min, max_value=prot_max, value=(prot_min, prot_max))
search_text = st.sidebar.text_input("Search for Food (e.g. burger, salad)", "")

filtered_df = full_df[(full_df['Caloric Value'] >= calories_range[0]) &
                      (full_df['Caloric Value'] <= calories_range[1]) &
                      (full_df['Protein'] >= protein_range[0]) &
                      (full_df['Protein'] <= protein_range[1])]

if search_text:
    suggestions = full_df['food'].dropna().unique()
    st.sidebar.write("Suggestions:", [s for s in suggestions if search_text.lower() in s.lower()][:5])
    filtered_df = filtered_df[filtered_df['food'].str.contains(search_text, case=False, na=False)]

# --- Header ---
st.title("🍔 Fast Food Nutrition Dashboard")
st.markdown("""
Analyze and visualize nutritional information from various fast food items. Use the tabs below to explore calories, protein, fat, sodium and more.
""")

# --- Download filtered CSV ---
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="filtered_nutrition.csv" class="download-button">📥 Download Filtered Data</a>'
    return href

st.markdown(get_table_download_link(filtered_df), unsafe_allow_html=True)

# --- Chart Selector ---
chart_type = st.radio("📊 Choose Chart to Display:", ["Overview Table", "Avg Calories, Sodium, Fat", "Protein Distribution", "Avg Calories by Food", "Fat-Calorie % by Source", "Nutrient Correlation Heatmap"], horizontal=True)

if chart_type == "Overview Table":
    st.subheader("📋 Filtered Data Preview")
    st.dataframe(filtered_df.head(20))

elif chart_type == "Avg Calories, Sodium, Fat":
    st.subheader("🍟 Average Calories, Sodium and Fat")
    fig1, ax1 = plt.subplots(figsize=(8, 4))
    filtered_df[['Caloric Value', 'Sodium', 'Fat']].mean().plot(kind='barh', ax=ax1, color=['#ffb366', '#fdd0a2', '#fdae6b'])
    ax1.set_title("Average Values of Calories, Sodium and Fat")
    ax1.set_xlabel("Amount")
    st.pyplot(fig1)

elif chart_type == "Protein Distribution":
    st.subheader("🍗 Protein Distribution")
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.histplot(filtered_df['Protein'], bins=30, kde=True, color="#a1d99b", ax=ax2)
    ax2.set_title("Distribution of Protein Values")
    ax2.set_xlabel("Protein (g)")
    st.pyplot(fig2)

elif chart_type == "Avg Calories by Food":
    st.subheader("📊 Average Calories by Food")
    avg_cal = filtered_df.groupby('food')['Caloric Value'].mean().sort_values(ascending=False).head(15)
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    avg_cal.plot(kind='bar', color='#ffcc99', ax=ax3)
    ax3.set_ylabel("Average Calories")
    ax3.set_title("Top 15 Foods by Average Caloric Value")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig3)

elif chart_type == "Fat-Calorie % by Source":
    st.subheader("🔥 Fat-Calorie % by Source")
    if 'FatCaloriesPercentage' in filtered_df.columns and 'Source File' in filtered_df.columns:
        avg_pct = filtered_df.groupby('Source File')['FatCaloriesPercentage'].mean().sort_values()
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        avg_pct.plot(kind='barh', color='#ffa366', ax=ax4)
        ax4.set_title("Fat-Calorie % by Source")
        st.pyplot(fig4)

elif chart_type == "Nutrient Correlation Heatmap":
    st.subheader("🧪 Nutrient Correlation Heatmap")
    corr = filtered_df[numeric_cols].corr()
    fig5, ax5 = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, cmap='Oranges', annot=True, fmt=".2f", linewidths=0.5, ax=ax5)
    ax5.set_title("Correlation Between Nutritional Variables")
    st.pyplot(fig5)

# --- Footer ---
st.markdown("---")
st.markdown("Made with ❤️ by Lee Lior · Reichman University 2025")


