import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="PCA Manufacturing Analytics Dashboard",
    layout="wide"
)

st.title("PCA-Based Manufacturing Analytics Dashboard for a Realtime Automated Filling Line")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Data Explorer", "PCA Insights"])

@st.cache_data
def load_data():
    return pd.read_csv("data/processed/cleaned_data.csv")

df = load_data()

# PAGE 1: OVERVIEW
if page == "Overview":
    st.header("Project Overview")
    st.markdown("""
    This dashboard visualises PCA insights from a realtime automated filling line.
    It supports variability analysis, anomaly detection, and continuous improvement.
    """)

# PAGE 2: DATA EXPLORER
elif page == "Data Explorer":
    st.header("Data Explorer")
    st.dataframe(df)

# PAGE 3: PCA INSIGHTS
elif page == "PCA Insights":
    st.header("PCA Insights")
    st.write("This section will show PCA scores, loadings, and explained variance.")

    # Load PCA results and limits
    pca_df = pd.read_csv("data/pca_results.csv")

    with open("data/limits.json", "r") as f:
        limits = json.load(f)

    T2_limit = limits["T2_limit"]
    Q_limit = limits["Q_limit"]

    # Sidebar filters
    st.sidebar.subheader("🔍 Filter PCA Data")

    part_ids = pca_df["Part_ID"].unique()
    selected_parts = st.sidebar.multiselect("Select Part ID(s):", part_ids, default=part_ids)

    if "Reject_Type" in pca_df.columns:
        reject_types = pca_df["Reject_Type"].dropna().unique()
        selected_rejects = st.sidebar.multiselect("Select Reject Type(s):", reject_types, default=reject_types)
    else:
        selected_rejects = None

    if "Timestamp" in pca_df.columns:
        pca_df["Timestamp"] = pd.to_datetime(pca_df["Timestamp"])
        min_date = pca_df["Timestamp"].min()
        max_date = pca_df["Timestamp"].max()
        selected_range = st.sidebar.slider("Select Timestamp Range:", min_date, max_date, (min_date, max_date))
    else:
        selected_range = None

    # Apply filters
    filtered_df = pca_df.copy()

    if selected_parts:
        filtered_df = filtered_df[filtered_df["Part_ID"].isin(selected_parts)]

    if selected_rejects is not None:
        filtered_df = filtered_df[filtered_df["Reject_Type"].isin(selected_rejects)]

    if selected_range is not None:
        filtered_df = filtered_df[
            (filtered_df["Timestamp"] >= selected_range[0]) &
            (filtered_df["Timestamp"] <= selected_range[1])
        ]

    # Preview filtered data
    st.write("Filtered PCA Data:")
    st.dataframe(filtered_df)
    
st.dataframe(filtered_df)

# KPI Tiles

st.subheader(" Key Performance Indicators")

# Calculate anomaly flags
filtered_df["T2_Flag"] = filtered_df["T2"] > T2_limit
filtered_df["Q_Flag"] = filtered_df["Q"] > Q_limit
filtered_df["Anomaly"] = filtered_df["T2_Flag"] | filtered_df["Q_Flag"]

total_parts = len(filtered_df)
total_anomalies = filtered_df["Anomaly"].sum()
pct_anomalies = (total_anomalies / total_parts * 100) if total_parts > 0 else 0

# Most common reject type
if "Reject_Type" in filtered_df.columns and filtered_df["Reject_Type"].notna().any():
    top_reject = filtered_df["Reject_Type"].mode()[0]
else:
    top_reject = "N/A"

# Display KPI tiles in 4 columns
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Parts", f"{total_parts}")
col2.metric("Total Anomalies", f"{total_anomalies}")
col3.metric("% Out of Control", f"{pct_anomalies:.2f}%")
col4.metric("Most Common Reject", top_reject)




