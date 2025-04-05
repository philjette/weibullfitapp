import streamlit as st
from streamlit_option_menu import option_menu

# Import pages as modules
from app_pages import (
    fitting_guided,
    point_based_fit,
    parameter_based_fit,
    historical_data_fit,
    fmea_based_fit
)

# Set page configuration
st.set_page_config(page_title="AssetX | Home", page_icon="📈", layout="wide")

# Sidebar navigation
with st.sidebar:

    st.logo("static_content/logo.png")
    selected_section = option_menu(
        "Menu",
        ["Home", "Curve Fitting", "FMEA"],
        icons=["house", "graph-up", "sliders"],
        #menu_icon="database",
        default_index=0
    )

    # Determine the subpage selection under "Fitting Methods" and "Data-Based Methods"
    selected_page = None
    if selected_section == "Curve Fitting":
        selected_page = st.radio("Choose a fitting method:", [
            "Point-Based Fit",
            "Parameter-Based Fit",
            "Guided Fit"
            "Historical Data Fit"
        ])
    elif selected_section == "FMEA":
        selected_page = st.radio("", [
            "FMEA Generation"
        ])

# Page routing
if selected_section == "Curve Fitting":
    if selected_page == "Point-Based Fit":
        point_based_fit.show()
    elif selected_page == "Parameter-Based Fit":
        parameter_based_fit.show()
    elif selected_page == "Guided Fit":
        fitting_guided.show()
    elif selected_page == "Historical Data Fit":
        fitting_guided.show()

elif selected_section == "Data-Based Methods":
    if selected_page == "FMEA Generation":
        fmea_based_fit.show()

else:
    # Default home content
    st.title("AI-Powered Reliability Tools")

    st.markdown("""
    AssetX provides a set of tools designed to help engineers and reliability professionals to optimize asset reliability through end-of-life modelling and failures modes and effects analysis. 
    
    Capabilities:
    - Generate failure curves using multiple fitting methods
    - Generate FMEAs based on asset characteristics and operating conditions 
    - Analyze the probability of failure over time
    - Compare different reliability models
    - Export data for further analysis
    
    ### Getting Started
    
    Navigate through the different pages using the sidebar menu to access various fitting methods:
    
    1. **Point-Based Fit**: Fit a curve by providing specific points on the cumulative distribution  
    2. **Direct Parameter Fit**: Input shape and scale parameters directly  
    3. **Guided Fit**: Answer questions about your assets to fit a general failure curve  
    4. **Historical Data Fit**: Upload a CSV file with asset data to fit a failure curve using statistical methods  
    5. **FMEA-based Fit**: Generate failure curves by failure mode based on an FMEA            
    """)

    st.info("Use the sidebar navigation to access the different fitting methods and tools.")

    st.markdown("""
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; font-size: 0.8em;'>
        Created by <a href='https://www.linkedin.com/in/philjette/' target='_blank'>Philippe Jette</a>
    </div>
    """, unsafe_allow_html=True)
