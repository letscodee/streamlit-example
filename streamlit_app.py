import streamlit as st
import numpy as np
from scipy.stats import proportions_ztest
import matplotlib.pyplot as plt

# Page title and layout
st.title("A/B Testing with Streamlit")
st.markdown("---")

# Generate random data
np.random.seed(123)  # Set a random seed for reproducibility
data_size = 100  # Number of data points
data = np.random.randint(2, size=data_size)

# Divide data into two groups
split_index = int(len(data) / 2)
group_1 = data[:split_index]
group_2 = data[split_index:]

# Perform statistical significance test
control_conversion_rate = np.mean(group_1)
treatment_conversion_rate = np.mean(group_2)
control_sample_size = len(group_1)
treatment_sample_size = len(group_2)

# Calculate statistical significance
z_score, p_value = proportions_ztest([np.sum(group_1), np.sum(group_2)], [control_sample_size, treatment_sample_size])

# Display results
st.subheader("A/B Test Results")

# Display conversion rates
col1, col2 = st.beta_columns(2)
with col1:
    st.metric("Control Conversion Rate", f"{control_conversion_rate:.2%}")
with col2:
    st.metric("Treatment Conversion Rate", f"{treatment_conversion_rate:.2%}")

st.markdown("---")

# Display statistical significance
st.metric("Z-Score", f"{z_score:.2f}")
st.metric("P-Value", f"{p_value:.4f}")

# Visualize conversion rates
labels = ["Control", "Treatment"]
conversion_rates = [control_conversion_rate, treatment_conversion_rate]
fig, ax = plt.subplots()
ax.bar(labels, conversion_rates, color=["skyblue", "lightgreen"])
ax.set_ylim([0, max(conversion_rates) * 1.2])
ax.set_ylabel("Conversion Rate")
ax.set_title("A/B Test Conversion Rates")
st.pyplot(fig)

st.markdown("---")

# Display statistical significance
st.metric("Z-Score", f"{z_score:.2f}")
st.metric("P-Value", f"{p_value:.4f}")

# Visualize conversion rates
labels = ["Control", "Treatment"]
conversion_rates = [control_cr, treatment_cr]
fig, ax = plt.subplots()
ax.bar(labels, conversion_rates, color=["skyblue", "lightgreen"])
ax.set_ylim([0, max(conversion_rates) * 1.2])
ax.set_ylabel("Conversion Rate")
ax.set_title("A/B Test Conversion Rates")
st.pyplot(fig)


