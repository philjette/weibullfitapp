import streamlit as st
from components.direct_params import direct_params_interface

st.title("Parameter-Based Fit")

# No login checks needed - all pages are accessible now

# Display main interface
st.title("Direct Parameter Fitting")
st.write("Directly input Weibull distribution parameters to generate a curve.")

# Call the direct parameter interface
direct_params_interface()

# Add footer
st.markdown("""
<div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; font-size: 0.8em;'>
    Created by <a href='https://www.linkedin.com/in/philjette/' target='_blank'>Philippe Jette</a>
</div>
""", unsafe_allow_html=True)