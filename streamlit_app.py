# import streamlit as st
# import numpy as np
# from statsmodels.stats.proportion import proportions_ztest
# import matplotlib.pyplot as plt

# # Page title and layout
# st.title("A/B Testing with Streamlit")
# st.markdown("---")

# # User input for conversion rates
# control_conversion_rate = st.number_input("Control Conversion Rate", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
# treatment_conversion_rate = st.number_input("Treatment Conversion Rate", min_value=0.0, max_value=100.0, value=12.0, step=0.1)

# # User input for sample sizes
# control_sample_size = st.number_input("Control Sample Size", min_value=1, value=100, step=1)
# treatment_sample_size = st.number_input("Treatment Sample Size", min_value=1, value=100, step=1)

# # Generate random customer IDs
# np.random.seed(123)  # Set a random seed for reproducibility
# control_group = np.random.choice(range(1000, 2000), size=int(control_sample_size), replace=False)
# treatment_group = np.random.choice(range(2000, 3000), size=int(treatment_sample_size), replace=False)

# # Perform statistical significance test
# z_score, p_value = proportions_ztest([control_conversion_rate, treatment_conversion_rate],
#                                      [control_sample_size, treatment_sample_size])

# # Display data divided into two groups
# st.subheader("Data Divided into Two Groups")

# col1, col2 = st.columns(2)
# with col1:
#     st.write("**Control Group (Group 1):**")
#     st.write(control_group)

# with col2:
#     st.write("**Treatment Group (Group 2):**")
#     st.write(treatment_group)

# st.markdown("---")

# # Display A/B test results
# st.subheader("A/B Test Results")

# # Display conversion rates
# col3, col4 = st.columns(2)
# with col3:
#     st.metric("Control Conversion Rate", f"{control_conversion_rate:.2f}%")
# with col4:
#     st.metric("Treatment Conversion Rate", f"{treatment_conversion_rate:.2f}%")

# st.markdown("---")

# # Display statistical significance
# st.metric("Z-Score", f"{z_score:.2f}")
# st.metric("P-Value", f"{p_value:.4f}")

# # Visualize conversion rates
# labels = ["Control", "Treatment"]
# conversion_rates = [control_conversion_rate, treatment_conversion_rate]
# fig, ax = plt.subplots()
# ax.bar(labels, conversion_rates, color=["skyblue", "lightgreen"])
# ax.set_ylim([0, max(conversion_rates) * 1.2])
# ax.set_ylabel("Conversion Rate")
# ax.set_title("A/B Test Conversion Rates")
# st.pyplot(fig)



import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats
from scipy.stats import norm
import altair as alt

st.set_page_config(
    page_title="A/B Test Comparison", page_icon="📈", initial_sidebar_state="expanded"
)


def conversion_rate(conversions, visitors):
    return (conversions / visitors) * 100


def lift(cra, crb):
    return ((crb - cra) / cra) * 100


def std_err(cr, visitors):
    return np.sqrt((cr / 100 * (1 - cr / 100)) / visitors)


def std_err_diff(sea, seb):
    return np.sqrt(sea ** 2 + seb ** 2)


def z_score(cra, crb, error):
    return ((crb - cra) / error) / 100


def p_value(z, hypothesis):
    if hypothesis == "One-sided" and z < 0:
        return 1 - norm().sf(z)
    elif hypothesis == "One-sided" and z >= 0:
        return norm().sf(z) / 2
    else:
        return norm().sf(z)


def significance(alpha, p):
    return "YES" if p < alpha else "NO"


def plot_chart(df):
    chart = (
        alt.Chart(df)
        .mark_bar(color="#61b33b")
        .encode(
            x=alt.X("Group:O", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Conversion:Q", title="Conversion rate (%)"),
            opacity="Group:O",
        )
        .properties(width=500, height=500)
    )

    chart_text = chart.mark_text(
        align="center", baseline="middle", dy=-10, color="black"
    ).encode(text=alt.Text("Conversion:Q", format=",.3g"))

    return st.altair_chart((chart + chart_text).interactive())


def style_negative(v, props=""):
    return props if v < 0 else None


def style_p_value(v, props=""):
    return np.where(v < st.session_state.alpha, "color:green;", props)


def calculate_significance(
    conversions_a, conversions_b, visitors_a, visitors_b, hypothesis, alpha
):
    st.session_state.cra = conversion_rate(int(conversions_a), int(visitors_a))
    st.session_state.crb = conversion_rate(int(conversions_b), int(visitors_b))
    st.session_state.uplift = lift(st.session_state.cra, st.session_state.crb)
    st.session_state.sea = std_err(st.session_state.cra, float(visitors_a))
    st.session_state.seb = std_err(st.session_state.crb, float(visitors_b))
    st.session_state.sed = std_err_diff(st.session_state.sea, st.session_state.seb)
    st.session_state.z = z_score(
        st.session_state.cra, st.session_state.crb, st.session_state.sed
    )
    st.session_state.p = p_value(st.session_state.z, st.session_state.hypothesis)
    st.session_state.significant = significance(
        st.session_state.alpha, st.session_state.p
    )


placeholder = st.empty()
placeholder.title("A/B Test Comparison")

with st.sidebar:

    uploaded_file = st.file_uploader("Upload CSV", type=".csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.markdown("#### Data preview")
        st.dataframe(df.head())

        ab = st.multiselect("A/B column", options=df.columns)
        if ab:
            control = df[ab[0]].unique()[0]
            treatment = df[ab[0]].unique()[1]
            decide = st.radio(f"Is {treatment} Variant B?", options=["Yes", "No"])
            if decide == "No":
                control, treatment = treatment, control
            visitors_a = df[ab[0]].value_counts()[control]
            visitors_b = df[ab[0]].value_counts()[treatment]

        result = st.multiselect("Result column", options=df.columns)

        if result:
            conversions_a = (
                df[[ab[0], result[0]]].groupby(ab[0]).agg("sum")[result[0]][control]
            )
            conversions_b = (
                df[[ab[0], result[0]]].groupby(ab[0]).agg("sum")[result[0]][treatment]
            )


with st.sidebar.form("parameters"):
    st.markdown("### Parameters")
    st.radio(
        "Hypothesis type",
        options=["One-sided", "Two-sided"],
        index=0,
        key="hypothesis",
        help="TBD",
    )
    st.slider(
        "Significance level (α)",
        min_value=0.01,
        max_value=0.10,
        value=0.05,
        step=0.01,
        key="alpha",
        help=" The probability of mistakenly rejecting the null hypothesis, if the null hypothesis is true. This is also called false positive and type I error. ",
    )
    submit = st.form_submit_button("Apply changes", on_click=None)

if submit:
    placeholder.empty()  # Remove title
    calculate_significance(
        conversions_a,
        conversions_b,
        visitors_a,
        visitors_b,
        st.session_state.hypothesis,
        st.session_state.alpha,
    )

    mcol1, mcol2 = st.beta_columns(2)

    with mcol1:
        st.metric(
            "Delta",
            value=f"{(st.session_state.crb - st.session_state.cra):.3g}%",
            delta=f"{(st.session_state.crb - st.session_state.cra):.3g}%",
        )

    with mcol2:
        st.metric("Significant?", value=st.session_state.significant)

    results_df = pd.DataFrame(
        {
            "Group": ["Control", "Treatment"],
            "Conversion": [st.session_state.cra, st.session_state.crb],
        }
    )
    plot_chart(results_df)

    table = pd.DataFrame(
        {
            "Converted": [conversions_a, conversions_b],
            "Total": [visitors_a, visitors_b],
            "% Converted": [st.session_state.cra, st.session_state.crb],
        },
        index=pd.Index(["Control", "Treatment"]),
    )

    st.write(table.style.format(formatter={("% Converted"): "{:.3g}%"}))

    metrics = pd.DataFrame(
        {
            "p-value": [st.session_state.p],
            "z-score": [st.session_state.z],
            "uplift": [st.session_state.uplift],
        },
        index=pd.Index(["Metrics"]),
    )

    st.write(
        metrics.style.format(
            formatter={("p-value", "z-score"): "{:.3g}", ("uplift"): "{:.3g}%"}
        )
        .applymap(style_negative, props="color:red;")
        .apply(style_p_value, props="color:red;", axis=1, subset=["p-value"])
    )
