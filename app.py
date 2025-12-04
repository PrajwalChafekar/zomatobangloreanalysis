import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Zomato Analysis",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TITLE SECTION ---
st.markdown(
    """
    <h1 style='text-align:center; color:#FF4B4B;'>🍽️ Zomato Location-wise Cost Analysis</h1>
    <p style='text-align:center; font-size:18px; color:#555;'>Explore restaurants, ratings, votes & average cost</p>
    """,
    unsafe_allow_html=True
)

# Load dataset
df = pd.read_csv("Zomato_Live.csv")

# --- SIDEBAR SETTINGS ---
st.sidebar.header("⚙️ Controls")

# Dropdown – Select location
locations = sorted(df["location"].dropna().unique())
selected_location = st.sidebar.selectbox("📍 Choose Location:", locations)

# Dropdown – Select color palette
color_palettes = [
    "viridis", "plasma", "inferno", "magma", "cividis",
    "coolwarm", "winter", "spring", "summer", "autumn",
    "Blues", "Greens", "Reds", "Purples"
]

selected_palette = st.sidebar.selectbox("🎨 Select Color Palette", color_palettes)

# Slider – Grading (brightness / saturation effect)
grading_factor = st.sidebar.slider("🌈 Color Grading Strength", 0.5, 2.0, 1.0)


# --- MAIN LOGIC ---
if selected_location:

    lo = df[df["location"] == selected_location]

    if lo.empty:
        st.warning("No data found for this location.")
    else:

        # Grouping
        gr = (
            lo.groupby("name")[["rate", "approx_cost", "votes"]]
            .mean()
            .nlargest(15, "rate")
            .reset_index()
        )

        # --- METRIC CARDS ROW ---
        col1, col2, col3 = st.columns(3)

        col1.metric("⭐ Avg Rating", f"{gr['rate'].mean():.2f}")
        col2.metric("💰 Avg Cost For Two", f"₹{int(gr['approx_cost'].mean())}")
        col3.metric("👍 Avg Votes", f"{int(gr['votes'].mean())}")

        st.markdown(
            f"<h2 style='color:#FF4B4B;'>🏆 Top 15 Restaurants in {selected_location}</h2>",
            unsafe_allow_html=True
        )

        # --- PLOT ---
        fig, ax = plt.subplots(figsize=(20, 8))

        # Apply palette and grading
        palette = sb.color_palette(selected_palette)
        palette = [(r * grading_factor, g * grading_factor, b * grading_factor) for r, g, b in palette]

        sb.barplot(x=gr["name"], y=gr["approx_cost"], palette=palette, ax=ax)

        ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize=10)
        ax.set_ylabel("Approx Cost (₹)", fontsize=14)
        ax.set_xlabel("Restaurant Name", fontsize=14)
        ax.set_title(f"Cost Comparison in {selected_location}", fontsize=18)

        st.pyplot(fig)

        # --- DATA TABLE ---
        with st.expander("📊 Show Table Data"):
            st.dataframe(gr.style.background_gradient(cmap="Oranges"))

        # --- RAW DATA ---
        with st.expander("📂 View Raw Filtered Dataset"):
            st.dataframe(lo)

