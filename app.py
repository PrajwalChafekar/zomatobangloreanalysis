import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

st.title("Zomato Location-wise Cost Analysis")

# Assuming df is already loaded earlier in your script
# If not, load it like:
# df = pd.read_csv("../Datasets/zomato.csv")

# Show available locations
st.write(df.location.unique())

# Streamlit input instead of Python input()
l = st.text_input("Enter Location Name:")

if l:
    lo = df[df.location == l]

    if lo.empty:
        st.warning("No data found for this location.")
    else:
        gr = (lo.groupby('name')[['rate', 'approx_cost', 'votes']]
                .mean()
                .nlargest(15, 'rate')
                .reset_index())

        plt.figure(figsize=(20, 8))
        plt.xticks(rotation=90)
        sb.barplot(x=gr.name, y=gr.approx_cost, palette='winter')

        st.pyplot(plt)

