import streamlit as st
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt

# Page title and layout
st.title("A/B Testing with Streamlit")
st.markdown("---")

# User input for conversion rates
control_conversion_rate = st.number_input("Control Conversion Rate", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
treatment_conversion_rate = st.number_input("Treatment Conversion Rate", min_value=0.0, max_value=100.0, value=12.0, step=0.1)

# User input for sample sizes
control_sample_size = st.number_input("Control Sample Size", min_value=1, value=100, step=1)
treatment_sample_size = st.number_input("Treatment Sample Size", min_value=1, value=100, step=1)

# Generate random data
np.random.seed(123)  # Set a random seed for reproducibility
data = np.concatenate([np.zeros(control_sample_size), np.ones(treatment_sample_size)])

# Randomly divide data into two groups
np.random.shuffle(data)
group_1 = data[:control_sample_size]
group_2 = data[control_sample_size:]

# Perform statistical significance test
control_cr = np.mean(group_1)
treatment_cr = np.mean(group_2)
z_score, p_value = proportions_ztest([np.sum(group_1), np.sum(group_2)], [control_sample_size, treatment_sample_size])

# Display results
st.subheader("A/B Test Results")

# Display conversion rates
# col1, col2 = st.beta_columns(2)
# with col1:
#     st.metric("Control Conversion Rate", f"{control_cr:.2%}")
# with col2:
#     st.metric("Treatment Conversion Rate", f"{treatment_cr:.2%}")

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

# col1, col2 = st.beta_columns(2)
# with col1:
#     st.metric("Control Conversion Rate", f"{control_conversion_rate:.2%}")
# with col2:
#     st.metric("Treatment Conversion Rate", f"{treatment_conversion_rate:.2%}")

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


