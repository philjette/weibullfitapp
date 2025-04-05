import streamlit as st
from components.guided_selection import guided_selection_interface


def show():
    st.title("Questionnaire-Based Fit")

    # No login checks needed - all pages are accessible now

    # Display main interface
    st.title("Guided Parameter Selection")
    st.write("Answer simple questions about your assets to determine appropriate Weibull parameters.")

    # Call the guided selection interface
    guided_selection_interface()

    # Add footer
    st.markdown("""
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; font-size: 0.8em;'>
        Created by <a href='https://www.linkedin.com/in/philjette/' target='_blank'>Philippe Jette</a>
    </div>
    """, unsafe_allow_html=True)