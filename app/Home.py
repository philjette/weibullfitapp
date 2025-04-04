import streamlit as st
from components.auth import login_signup, logout
from utils.curve_storage import initialize_storage
from utils.page_config import configure_page_visibility

def main():
    """Home page of WeibullFitPro application."""
    st.set_page_config(
        page_title="WeibullFitPro | Home",
        page_icon="📈",
        layout="wide"
    )
    
    # Configure page visibility based on authentication
    configure_page_visibility()

    # Initialize database storage
    initialize_storage()

    # Authentication
    if not st.session_state.get("user_id") and not st.session_state.get("is_guest"):
        login_signup()
        # Add footer even on login page
        st.markdown("""
        <div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; font-size: 0.8em;'>
            Created by <a href='https://www.linkedin.com/in/philjette/' target='_blank'>Philippe Jette</a>
        </div>
        """, unsafe_allow_html=True)
        return

    # Show logout button in sidebar
    logout()

    # Welcome screen content for logged-in users
    st.title("Welcome to WeibullFitPro")
    
    # Updated app description (summary blurb)
    st.markdown("""
    ## About WeibullFitPro
    
    WeibullFitPro is a powerful statistical modeling application designed to help engineers and reliability professionals analyze asset life and failure probability through advanced Weibull distribution modeling. 
    
    With WeibullFitPro, you can:
    - Generate Weibull curves using multiple fitting methods
    - Analyze the probability of failure over time
    - Compare different reliability models
    - Export data for further analysis
    - Save your models for future reference
    
    ### Getting Started
    
    Navigate through the different pages using the sidebar menu to access various fitting methods:
    
    1. **Point-Based Fit**: Fit a curve by providing specific points on the cumulative distribution
    2. **Direct Parameter Fit**: Input shape and scale parameters directly
    3. **Guided Fit**: Answer questions about your assets to determine appropriate parameters
    4. **MLE Fitting**: Upload a CSV file with asset data to calculate parameters using statistical methods
    
    """)
    
    # Show guest mode warning if applicable
    if st.session_state.get("is_guest"):
        st.warning("⚠️ You are in Guest Mode: Save and download features are disabled. Log in to access all features.")

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