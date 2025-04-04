import streamlit as st
from components.direct_params import direct_params_interface

st.set_page_config(
    page_title="Direct Parameter Fit | WeibullFitPro",
    page_icon="🔢",
    layout="wide"
)

# Check if user is logged in
if "user_id" not in st.session_state and not st.session_state.get("is_guest"):
    st.warning("Please log in or continue as guest from the home page.")
    st.stop()

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