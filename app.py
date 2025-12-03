import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

st.set_page_config(page_title="Zomato Analysis", layout="wide")

st.title("🍽️ Zomato Location-wise Cost Analysis")

# Load dataset
df = pd.read_csv("Zomato_Live.csv")

# Unique locations
locations = sorted(df["location"].dropna().unique())

# Sidebar controls
st.sidebar.header("⚙️ Controls")

# Dropdown for location
l = st.sidebar.selectbox("Select Location:", locations)

# Choose palette
palette_choice = st.sidebar.selectbox(
    "Color Theme:",
    ["viridis", "magma", "coolwarm", "winter", "plasma", "cubehelix"]
)

# Sorting choice
sort_by = st.sidebar.radio(
    "Sort Restaurants By:",
    ["rate", "approx_cost", "votes"]
)

# Number of restaurants to display
top_n = st.sidebar.slider("Number of Restaurants:", 5, 25, 15)

# Checkbox for showing raw filtered data
show_raw = st.sidebar.checkbox("Show Raw Data", False)


# Main content
if l:
    lo = df[df["location"] == l]

    if lo.empty:
        st.warning("No data found for this location.")
    else:
        st.success(f"Showing results for **{l}**")

        # Grouping
        gr = (
            lo.groupby("name")[["rate", "approx_cost", "votes"]]
            .mean()
            .nlargest(top_n, sort_by)
            .reset_index()
        )

        # Optional raw table
        if show_raw:
            with st.expander("📄 Raw Filtered Data"):
                st.dataframe(lo)

        st.subheader(f"Top {top_n} Restaurants in {l} — Sorted by {sort_by.title()}")

        # Plot
        fig, ax = plt.subplots(figsize=(20, 8))
        sb.barplot(x=gr["name"], y=gr["approx_cost"], palette=palette_choice, ax=ax)

        ax.set_title(f"Average Cost for Two — {l}", fontsize=18, weight="bold")
        ax.set_xlabel("Restaurant Name", fontsize=14)
        ax.set_ylabel("Approx Cost", fontsize=14)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

        st.pyplot(fig)

        # Table expander
        with st.expander("📊 View Processed Table"):
            st.dataframe(gr)
