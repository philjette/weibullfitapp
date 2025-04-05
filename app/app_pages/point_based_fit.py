import streamlit as st
from components.point_fitting import point_fitting_interface

def show():
    """Display the Point-Based Fit page"""
    
    st.title("Point-Based Fit")

    # Display introduction
    st.write("Fit a Weibull curve by providing points on the cumulative distribution function.")
    
    # Call the point fitting interface
    point_fitting_interface()

    # Add footer
    st.markdown("""
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; font-size: 0.8em;'>
        Created by <a href='https://www.linkedin.com/in/philjette/' target='_blank'>Philippe Jette</a>
    </div>
    """, unsafe_allow_html=True)