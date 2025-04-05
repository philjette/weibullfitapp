import streamlit as st
from utils.page_config import configure_page_visibility

def main():
    """Home of AI-powered reliability analysis"""

    st.set_page_config(
        page_title="WeibullFit | Home",
        page_icon="📈",
        layout="wide"
    )

    # Configure page visibility without authentication
    if "show_all_pages" not in st.session_state:
        configure_page_visibility()

    # Welcome screen content
    st.title("AI powered reliability analysis")
    
    # App description (summary blurb)
    st.markdown("""
    
    Weibullfit is a powerful statistical modeling application designed to help engineers and reliability professionals analyze asset life and failure probability through advanced Weibull distribution modeling. 
    
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
    5. **FMEA-based fit**: Generate failure curves by failure mode based on an FMEA            
    
    """)
    
    # Add helpful information about navigation
    st.info("Use the sidebar navigation to access the different fitting methods and tools.")

    # Add footer
    st.markdown("""
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; font-size: 0.8em;'>
        Created by <a href='https://www.linkedin.com/in/philjette/' target='_blank'>Philippe Jette</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()