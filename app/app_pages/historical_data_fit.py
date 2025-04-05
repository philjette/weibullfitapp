import streamlit as st
from components.mle_fitting import mle_fitting_interface

def show():
    st.title("Historical Data Fit")

    # No login checks needed - all pages are accessible now

    # Display main interface
    st.title("Maximum Likelihood Estimation (MLE) Fitting")
    st.write("Upload a CSV file with asset data and fit a Weibull curve using statistical Maximum Likelihood Estimation.")

    # Call the MLE fitting interface
    mle_fitting_interface()

    # Add footer
    st.markdown("""
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; font-size: 0.8em;'>
        Created by <a href='https://www.linkedin.com/in/philjette/' target='_blank'>Philippe Jette</a>
    </div>
    """, unsafe_allow_html=True)