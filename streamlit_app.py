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

# Generate random customer IDs
np.random.seed(123)  # Set a random seed for reproducibility
control_group = np.random.choice(range(1000, 2000), size=int(control_sample_size), replace=False)
treatment_group = np.random.choice(range(2000, 3000), size=int(treatment_sample_size), replace=False)

# Perform statistical significance test
z_score, p_value = proportions_ztest([control_conversion_rate, treatment_conversion_rate],
                                     [control_sample_size, treatment_sample_size])

# Display data divided into two groups
st.subheader("Data Divided into Two Groups")

col1, col2 = st.columns(2)
with col1:
    st.write("**Control Group (Group 1):**")
    st.write(control_group)

with col2:
    st.write("**Treatment Group (Group 2):**")
    st.write(treatment_group)

st.markdown("---")

# Display A/B test results
st.subheader("A/B Test Results")

# Display conversion rates
col3, col4 = st.columns(2)
with col3:
    st.metric("Control Conversion Rate", f"{control_conversion_rate:.2f}%")
with col4:
    st.metric("Treatment Conversion Rate", f"{treatment_conversion_rate:.2f}%")

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

