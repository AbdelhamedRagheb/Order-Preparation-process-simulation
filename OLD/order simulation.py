import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import time

# Set page config
st.set_page_config(page_title="Order Processing Simulation", layout="wide")

# Sidebar Inputs
st.sidebar.title("Simulation Settings")
num_orders = st.sidebar.slider("Number of Orders", 1, 100, 20)
stage_times = {
    "Received": st.sidebar.slider("Received Time (s)", 1, 5, 1),
    "Preparing": st.sidebar.slider("Preparing Time (s)", 1, 10, 3),
    "Packaging": st.sidebar.slider("Packaging Time (s)", 1, 8, 2),
    "Delivery": st.sidebar.slider("Delivery Time (s)", 1, 10, 4)
}

st.title("📦 Order Processing System Simulation")
st.markdown("""This simulation models how an order progresses through the stages: 
**Received → Preparing → Packaging → Delivery**. 
We show order times, queue bottlenecks, and distribution of total processing time.""")

# Simulate Orders
processing_data = []

progress_bar = st.progress(0)
status_text = st.empty()

for i in range(num_orders):
    order_id = f"Order-{i+1}"
    order_record = {"OrderID": order_id}
    total_time = 0
    for stage, stage_time in stage_times.items():
        total_time += stage_time + np.random.normal(0, 0.5)  # Add small variation
        order_record[stage] = total_time
    order_record["TotalTime"] = total_time
    processing_data.append(order_record)
    progress_bar.progress((i + 1) / num_orders)
    status_text.text(f"Processing {order_id}...")
    time.sleep(0.02)

status_text.text("Simulation complete!")
df = pd.DataFrame(processing_data)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Average Time per Stage")
    stage_means = df[[s for s in stage_times]].mean()
    fig1, ax1 = plt.subplots()
    sns.barplot(x=stage_means.index, y=stage_means.values, palette="Blues_d", ax=ax1)
    ax1.set_ylabel("Average Time (s)")
    st.pyplot(fig1)

with col2:
    st.subheader("⏱️ Total Processing Time per Order")
    fig2, ax2 = plt.subplots()
    sns.histplot(df["TotalTime"], bins=10, kde=True, color="skyblue", ax=ax2)
    ax2.set_xlabel("Total Time (s)")
    st.pyplot(fig2)

st.subheader("📈 Queue Dynamics Over Time")
fig3, ax3 = plt.subplots()
for stage in stage_times:
    sns.lineplot(x=range(len(df)), y=df[stage], label=stage, ax=ax3)
ax3.set_xlabel("Order Index")
ax3.set_ylabel("Time Reached (s)")
st.pyplot(fig3)

st.subheader("📋 Sample Order Processing Data")
st.dataframe(df.head(10))
