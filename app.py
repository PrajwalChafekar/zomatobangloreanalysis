import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Zomato Cost Analysis",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ CUSTOM CSS FOR UI ------------------
st.markdown("""
<style>
/* Smooth hover animation for select boxes */
.stSelectbox div[data-baseweb="select"] {
    transition: 0.3s;
}
.stSelectbox div[data-baseweb="select"]:hover {
    transform: scale(1.02);
}

/* Card-like container */
.custom-box {
    background: #ffffffAA;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.15);
    margin-bottom: 25px;
}

/* Gradient title */
h1 {
    background: -webkit-linear-gradient(45deg, #ff4b1f, #1fddff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 900;
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("🍽️ Zomato Location-Wise Cost Analysis")

# ------------------ LOAD DATA ------------------
df = pd.read_csv("Zomato_Live.csv")

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.header("⚙️ Controls")

    # Top restaurant limit slider
    top_n = st.slider("Select number of top restaurants:", 5, 30, 15)

    # Color palette selection
    color_theme = st.selectbox(
        "Choose Color Theme:",
        ["Viridis", "Cividis", "Plasma", "Inferno", "Turbo", "Teal", "Aggrnyl"]
    )

    st.markdown("### 🎨 Selected Theme:")
    st.color_picker("Preview (does not change plot)", "#00aaff")

# ------------------ LOCATION SELECT ------------------
locations = sorted(df["location"].dropna().unique())

st.subheader("📍 Choose a Location")
l = st.selectbox("Select Location:", locations, key="location_select")

if l:
    lo = df[df["location"] == l]

    if lo.empty:
        st.warning("⚠️ No data found for this location.")
    else:
        # ------------------ GROUPING ------------------
        gr = (
            lo.groupby("name")[["rate", "approx_cost", "votes"]]
            .mean()
            .nlargest(top_n, "rate")
            .reset_index()
        )

        st.markdown(f"### ⭐ Top **{top_n} Restaurants** in **{l}** by Rating")

        # ------------------ ANIMATED INTERACTIVE BAR CHART ------------------
        fig = px.bar(
            gr,
            x="name",
            y="approx_cost",
            color="approx_cost",
            color_continuous_scale=color_theme.lower(),
            title=f"Cost Comparison of Top {top_n} Restaurants in {l}",
            animation_frame="rate",
            labels={"approx_cost": "Approx Cost (₹)", "name": "Restaurant"},
        )

        fig.update_layout(
            xaxis_tickangle=90,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=14),
            transition_duration=600
        )

        st.plotly_chart(fig, use_container_width=True)

        # ------------------ DATA TABLE ------------------
        with st.expander("📊 Show Data Table"):
            st.dataframe(gr.style.highlight_max("rate", color="lightgreen"))

        # ------------------ EXTRA ANIMATED LINE CHART ------------------
        st.markdown("### 📈 Votes vs Rating Trend (Animated)")
        fig2 = px.scatter(
            gr,
            x="rate",
            y="votes",
            size="approx_cost",
            color="rate",
            color_continuous_scale=color_theme.lower(),
            animation_frame="name",
            title="Votes vs Rating (Bubble Animation)"
        )
        st.plotly_chart(fig2, use_container_width=True)

