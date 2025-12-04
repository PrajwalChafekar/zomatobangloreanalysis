import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sb

# ----------------------------- PAGE CONFIG ------------------------------------
st.set_page_config(
    page_title="Zomato Explorer",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------- PAGE HEADER ------------------------------------
st.markdown(
    """
    <h1 style='text-align:center; color:#FF6347;'>🍽️ Zomato Location-wise Restaurant Analysis</h1>
    <p style='text-align:center; font-size:18px;'>
        Explore restaurant ratings, costs, and votes with interactive charts & colorful UI.
    </p>
    <hr>
    """,
    unsafe_allow_html=True,
)

# ----------------------------- LOAD DATA --------------------------------------
df = pd.read_csv("Zomato_Live.csv")

# Dropdown list
locations = sorted(df["location"].dropna().unique())

# ----------------------------- SIDEBAR UI -------------------------------------
st.sidebar.header("🔍 Filters & Options")

selected_location = st.sidebar.selectbox("Select Location", locations, help="Choose a location to explore")

chart_type = st.sidebar.radio(
    "Choose Chart Type",
    ["Bar Chart", "Line Chart", "Scatter Plot"],
    help="Switch between chart styles"
)

color_scheme = st.sidebar.color_picker("Choose Bar Color", "#1f77b4")

min_votes = st.sidebar.slider(
    "Minimum Votes", 
    int(df.votes.min()), 
    int(df.votes.max()), 
    0
)

# ----------------------------- FILTER DATA ------------------------------------
if selected_location:
    lo = df[df["location"] == selected_location]
    lo = lo[lo["votes"] >= min_votes]

    if lo.empty:
        st.warning("No data found for this location based on filters.")
    else:
        gr = (
            lo.groupby("name")[["rate", "approx_cost", "votes"]]
            .mean()
            .sort_values(by="rate", ascending=False)
            .head(15)
            .reset_index()
        )

        # ----------------------------- METRIC CARDS ------------------------------------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("⭐ Avg Rating", round(gr["rate"].mean(), 2))
        with col2:
            st.metric("💰 Avg Cost", int(gr["approx_cost"].mean()))
        with col3:
            st.metric("🗳️ Avg Votes", int(gr["votes"].mean()))

        st.markdown(f"### 🎯 Top 15 Restaurants in **{selected_location}**")

        # ----------------------------- PLOTLY CHARTS ------------------------------------
        if chart_type == "Bar Chart":
            fig = px.bar(
                gr,
                x="name",
                y="approx_cost",
                color="rate",
                color_continuous_scale="Teal_r",
                title=f"Cost for Two People in {selected_location}",
                height=550
            )
        elif chart_type == "Line Chart":
            fig = px.line(
                gr,
                x="name",
                y="approx_cost",
                markers=True,
                title=f"Cost Trend for Restaurants in {selected_location}",
                height=550
            )
            fig.update_traces(line_color=color_scheme)
        else:
            fig = px.scatter(
                gr,
                x="rate",
                y="approx_cost",
                size="votes",
                hover_name="name",
                color="rate",
                title=f"Rate vs Cost Scatter - {selected_location}",
                color_continuous_scale="thermal",
                height=550
            )

        fig.update_layout(xaxis_title="Restaurant Name", yaxis_title="Approx Cost")

        st.plotly_chart(fig, use_container_width=True)

        # ----------------------------- DATA TABLE ------------------------------------
        with st.expander("📄 Show Full Restaurant Table"):
            st.dataframe(gr.style.highlight_max(axis=0, color="lightgreen"))


