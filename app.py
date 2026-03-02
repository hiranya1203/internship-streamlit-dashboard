import streamlit as st
import pandas as pd

# Page Title
st.title("Bank Customer Churn Dashboard")

# Load Data
df = pd.read_csv("European_Bank.csv")

# ---------------- SIDEBAR FILTERS ---------------- #

st.sidebar.header("Filter Options")

# Geography Filter
selected_geo = st.sidebar.multiselect(
    "Select Geography",
    options=df['Geography'].unique(),
    default=df['Geography'].unique()
)

# Gender Filter
selected_gender = st.sidebar.multiselect(
    "Select Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

# Apply Filters
filtered_df = df[
    (df['Geography'].isin(selected_geo)) &
    (df['Gender'].isin(selected_gender))
]

# ---------------- KPI CALCULATIONS ---------------- #

# Overall Churn Rate
overall_churn = filtered_df['Exited'].mean() * 100

# High-Value Customers (Top 25% Balance)
threshold = filtered_df['Balance'].quantile(0.75)
high_value = filtered_df[filtered_df['Balance'] >= threshold]
high_value_churn = high_value['Exited'].mean() * 100

# Geographic Risk Index
geo_churn = filtered_df.groupby('Geography')['Exited'].mean() * 100
geo_risk_index = geo_churn / overall_churn
highest_geo_risk = geo_risk_index.max()

# Engagement Risk Ratio
engagement = filtered_df.groupby('IsActiveMember')['Exited'].mean() * 100
active_churn = engagement[1]
inactive_churn = engagement[0]
engagement_ratio = inactive_churn / active_churn

# ---------------- KPI DISPLAY ---------------- #

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Overall Churn Rate", f"{overall_churn:.2f}%")
col2.metric("High-Value Churn Rate", f"{high_value_churn:.2f}%")
col3.metric("Highest Geo Risk Index", f"{highest_geo_risk:.2f}")
col4.metric("Engagement Risk Ratio", f"{engagement_ratio:.2f}x")

# ---------------- CHURN BY CREDIT SCORE BAND ---------------- #
# ---------------- CREDIT SCORE BANDS ---------------- #

bins = [300, 580, 670, 740, 850]
labels = ["Poor", "Fair", "Good", "Excellent"]

filtered_df = filtered_df.copy()

filtered_df["CreditScoreBand"] = pd.cut(
    filtered_df["CreditScore"],
    bins=bins,
    labels=labels
)

st.subheader("Churn Rate by Credit Score Band")

credit_churn = (
    filtered_df
    .groupby("CreditScoreBand")["Exited"]
    .mean() * 100
)

st.bar_chart(credit_churn)

# ---------------- CHURN BY GEOGRAPHY ---------------- #

st.subheader("Churn Rate by Geography")

geo_churn = (
    filtered_df
    .groupby("Geography")["Exited"]
    .mean()
    .sort_values(ascending=False) * 100
)

st.bar_chart(geo_churn)

# ---------------- CHURN BY GENDER ---------------- #

st.subheader("Churn Rate by Gender")

gender_churn = (
    filtered_df
    .groupby("Gender")["Exited"]
    .mean() * 100
)

st.bar_chart(gender_churn)


