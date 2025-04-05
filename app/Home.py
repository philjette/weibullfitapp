import streamlit as st
from utils.page_config import configure_page_visibility
from streamlit_option_menu import option_menu

# Configure page settings at the top
st.set_page_config(
    page_title="WeibullFit | Home",
    page_icon="📈",
    layout="wide"
)

def main():
    """Home of AI-powered reliability analysis"""

    # Configure page visibility without authentication
    if "show_all_pages" not in st.session_state:
        configure_page_visibility()

    # Sidebar navigation using option_menu
    with st.sidebar:
        selected_section = option_menu(
            "📈 WeibullFit Menu",
            ["Fitting Methods", "Data-Based Methods"],
            icons=["tools", "database"],
            menu_icon="cast",
            default_index=0
        )

        if selected_section == "Fitting Methods":
            selected_page = st.radio("Choose a fitting method:", [
                "Point-Based Fit",
                "Parameter-Based Fit",
                "Guided Fit"
            ])
        elif selected_section == "Data-Based Methods":
            selected_page = st.radio("Choose a data-based method:", [
                "Historical Data Fit",
                "FMEA-Based Fit"
            ])
        else:
            selected_page = None

    # Page routing based on selection
    if selected_section == "Fitting Methods":
        if selected_page == "Point-Based Fit":
            st.switch_page("app_pages/1_Fitting_Point_Based.py")
        elif selected_page == "Parameter-Based Fit":
            st.switch_page("app_pages/2_Fitting_Parameter_Based.py")
        elif selected_page == "Guided Fit":
            st.switch_page("app_pages/3_Fitting_Guided.py")

    elif selected_section == "Data-Based Methods":
        if selected_page == "Historical Data Fit":
            st.switch_page("app_pages/4_Data_Historical.py")
        elif selected_page == "FMEA-Based Fit":
            st.switch_page("app_pages/5_FMEA_Based.py")

    # Welcome screen content (only shown when on Home)
    st.title("AI powered reliability analysis")

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
    5. **FMEA-based Fit**: Generate failure curves by failure mode based on an FMEA            
    """)

    st.info("Use the sidebar navigation to access the different fitting methods and tools.")

    st.markdown("""
    <div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; font-size: 0.8em;'>
        Created by <a href='https://www.linkedin.com/in/philjette/' target='_blank'>Philippe Jette</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
