import streamlit as st
from src.testdesign import design_binomial_experiment
from src.datagen import ABTestGenerator
from src.plots import plot_ctr, plot_views, plot_p_hist_all, plot_power, plot_p_cdf_all
from src.utils import apply_tests
from src.tests import t_test_clicks, t_test_ctr, mw_test, binom_test, bootstrap_test
import numpy as np

# Define global variables to store the results
result_dict_aa = None
result_dict_ab = None
p_vals_aa = None
p_vals_ab = None


def main():
    global result_dict_aa, result_dict_ab, p_vals_aa, p_vals_ab

    # Set page configuration
    st.set_page_config(
        page_title="A/B Test Simulator",
        layout="wide",  # Use wide layout for better visualization
        menu_items={
            "Get Help": "https://github.com/Defalt-Meh/A-B-TEST-TOOL",
            "About": "Simulate and analyze A/B tests.",
        }
    )

    # Sidebar for parameters
    st.sidebar.title("Data Generation Model")
    st.sidebar.markdown("### Simulation Parameters")
    with st.sidebar.form("Data Generation Model"):
        base_ctr_pcnt = st.slider("Base CTR (%)", 0.1, 20.0, 2.0, 0.1)
        uplift_pcnt = st.slider("CTR Uplift (%)", 0.1, 10.0, 0.4, 0.1)
        skew = st.slider("Views Skew", 0.1, 4.0, 0.6, 0.1)
        ctr_beta = st.slider("CTR Beta (Shape Parameter)", 1, 2000, 1000, 1)
        sb_submit_button = st.form_submit_button("Apply Changes")

    # Main page title
    st.title("A/B Test Simulator")

    # Experiment Design Section
    st.subheader("1. Experiment Design")
    with st.form("Experiment Design"):
        col1, col2, col3 = st.columns(3)
        alpha = col1.slider("Alpha (Type I Error)", 0.01, 0.2, 0.05, 0.01)
        beta = col2.slider("Beta (Type II Error)", 0.01, 0.8, 0.2, 0.01)
        mde = col3.slider("Minimum Detectable Effect (%)", 0.1, 10.0, 0.4, 0.1)
        n_samples = col1.slider("Sample Size per Group", 100, 10000, 1000, 100)
        ed_submit = st.form_submit_button("Estimate Experiment")

    if sb_submit_button or ed_submit:
        uplift = uplift_pcnt / 100
        base_ctr = base_ctr_pcnt / 100
        mde = mde / 100

        datagen_aa = ABTestGenerator(base_ctr, 0, ctr_beta, skew)
        datagen_ab = ABTestGenerator(base_ctr, uplift, ctr_beta, skew)

        result_dict_aa = datagen_aa.generate_n_experiment(n_samples, 500)
        result_dict_ab = datagen_ab.generate_n_experiment(n_samples, 500)

        clicks_0 = result_dict_aa["clicks_0"][0]
        views_0 = result_dict_aa["views_0"][0]
        estimated_ctr_h0 = np.sum(clicks_0) / np.sum(views_0)

        min_samples_required = design_binomial_experiment(
            mde=mde,
            p_0=estimated_ctr_h0,
            alpha=alpha,
            beta=beta,
        )

        st.markdown(
            f"""
            **Sample Size Calculations:**
            - Base CTR: **{base_ctr:.2%}**
            - Minimum Detectable Effect: **{mde:.2%}**
            - Alpha (Type I Error): **{alpha:.2f}**
            - Beta (Type II Error): **{beta:.2f}**
            - **Estimated Minimal Interactions Required: {min_samples_required}**
            """
        )

    # Ground Truth Distributions
    if result_dict_aa:
        st.divider()
        st.subheader("2. Ground Truth Distributions")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Data Distributions under H0 (No Effect)")
            plot_ctr(result_dict_aa, 0)
            plot_views(result_dict_aa, 0)
        with col2:
            st.write("Data Distributions under H1 (With Effect)")
            plot_ctr(result_dict_ab, 0)
            plot_views(result_dict_ab, 0)

    # A/A and A/B Test Results
    if result_dict_aa and result_dict_ab:
        st.divider()
        st.subheader("3. A/A and A/B Test Results")
        p_vals_aa = apply_tests(result_dict_aa, {
            "T-test (Clicks)": t_test_clicks,
            "T-test (CTR)": t_test_ctr,
            "Mann–Whitney (Clicks)": mw_test,
            "Binomial (CTR)": binom_test,
            "Bootstrap (CTR)": bootstrap_test,
        })

        p_vals_ab = apply_tests(result_dict_ab, {
            "T-test (Clicks)": t_test_clicks,
            "T-test (CTR)": t_test_ctr,
            "Mann–Whitney (Clicks)": mw_test,
            "Binomial (CTR)": binom_test,
            "Bootstrap (CTR)": bootstrap_test,
        })

        col1, col2 = st.columns(2)
        with col1:
            st.write("A/A Test Results")
            plot_p_hist_all(p_vals_aa)
            plot_p_cdf_all(p_vals_aa)
        with col2:
            st.write("A/B Test Results")
            plot_p_hist_all(p_vals_ab)
            plot_p_cdf_all(p_vals_ab)

        # Power Calculation
        st.divider()
        st.subheader("4. Statistical Power")
        plot_power(p_vals_ab, alpha=alpha)

if __name__ == "__main__":
    main()
