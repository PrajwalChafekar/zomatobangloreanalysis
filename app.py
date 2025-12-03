import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

st.title("Zomato Location-wise Cost Analysis")

# Load dataset
df = pd.read_csv("Zomato_Live.csv")

# Get unique locations sorted
locations = sorted(df.location.dropna().unique())

# Dropdown for location selection
l = st.selectbox("Select Location:", locations)

if l:
    lo = df[df.location == l]

    if lo.empty:
        st.warning("No data found for this location.")
    else:
        gr = (lo.groupby('name')[['rate', 'approx_cost', 'votes']]
                .mean()
                .nlargest(15, 'rate')
                .reset_index())

        st.subheader(f"Top 15 Restaurants in {l} by Rating")

        fig, ax = plt.subplots(figsize=(20, 8))
        sb.barplot(x=gr.name, y=gr.approx_cost, palette='winter', ax=ax)
        plt.xticks(rotation=90)

        st.pyplot(fig)

        # Optional: show table
        with st.expander("Show Data Table"):
            st.dataframe(gr)
