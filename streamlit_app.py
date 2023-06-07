
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

# Perform statistical significance test
control_data = np.random.binomial(1, control_conversion_rate / 100, control_sample_size)
treatment_data = np.random.binomial(1, treatment_conversion_rate / 100, treatment_sample_size)

# Calculate conversion rates
control_cr = np.mean(control_data)
treatment_cr = np.mean(treatment_data)

# Calculate statistical significance
z_score, p_value = proportions_ztest([np.sum(control_data), np.sum(treatment_data)], [control_sample_size, treatment_sample_size])

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


