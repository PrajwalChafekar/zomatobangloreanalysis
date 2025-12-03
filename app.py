import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

st.set_page_config(page_title="Zomato Analysis", layout="wide")

st.title("🍽️ Zomato Restaurant Analysis Dashboard")

# Load Data
df = pd.read_csv("../Datasets/zomato.csv")

# Drop unnecessary columns
df = df.drop(['url','address','phone','dish_liked','menu_item','reviews_list',
              'listed_in(type)','listed_in(city)'], axis=1)

# Rename cost column
df = df.rename(columns={'approx_cost(for two people)':'approx_cost'})

# Fill NA
df = df.fillna(0)

# Clean 'rate'
df.rate = df.rate.replace('[/5]', '', regex=True)
df.rate = df.rate.replace(['NEW', 'nan', '-'], 0)
df.rate = df.rate.astype('float64')

# Clean cost
df.approx_cost = df.approx_cost.replace('[,]', '', regex=True).astype('int64')

# Sidebar
st.sidebar.header("Filters")

locations = sorted(df.location.unique())
location_selected = st.sidebar.selectbox("Select Location", locations)

# Filter data
filtered = df[df.location == location_selected]

# Group & sort
gr = filtered.groupby('name')[['rate','approx_cost','votes']].mean() \
             .nlargest(15, 'rate').reset_index()

st.subheader(f"Top 15 Restaurants in **{location_selected}** by Rating")

# Plot
fig, ax = plt.subplots(figsize=(18, 6))
sb.barplot(x=gr.name, y=gr.approx_cost, palette='winter', ax=ax)
plt.xticks(rotation=90)
plt.ylabel("Approx Cost for Two")

st.pyplot(fig)

# Show data preview
with st.expander("Show Processed Data"):
    st.dataframe(gr)
