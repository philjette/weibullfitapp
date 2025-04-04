import streamlit as st
from utils.page_config import configure_page_visibility

def main():
    """Home page of WeibullFitPro application."""
    st.set_page_config(
        page_title="WeibullFitPro | Home",
        page_icon="📈",
        layout="wide"
    )
    
    # Configure page visibility without authentication
    if "show_all_pages" not in st.session_state:
        configure_page_visibility()

    # Welcome screen content
    st.title("Welcome to WeibullFitPro")
    
    # App description (summary blurb)
    st.markdown("""
    ## About WeibullFitPro
    
    WeibullFitPro is a powerful statistical modeling application designed to help engineers and reliability professionals analyze asset life and failure probability through advanced Weibull distribution modeling. 
    
    With WeibullFitPro, you can:
    - Generate Weibull curves using multiple fitting methods
    - Analyze the probability of failure over time
    - View different probability distribution functions
    - Export data for further analysis
    
    ### Getting Started
    
    Navigate through the different pages using the sidebar menu to access various fitting methods:
    
    1. **Point-Based Fit**: Fit a curve by providing specific points on the cumulative distribution
    2. **Direct Parameter Fit**: Input shape and scale parameters directly
    3. **Guided Fit**: Answer questions about your assets to determine appropriate parameters
    4. **MLE Fitting**: Upload a CSV file with asset data to calculate parameters using statistical methods
    
    ### About Statistical Concepts
    
    <details>
    <summary>Click to learn about key statistical concepts</summary>
    
    #### Weibull Distribution
    A versatile distribution used to model the lifetime of assets and predict failure rates. It's particularly useful for reliability engineering and maintenance planning.
    
    #### Probability Density Function (PDF)
    Shows how likely different failure times are. Think of it as a "probability map" showing which ages are most common for failures to occur.
    
    #### Cumulative Distribution Function (CDF)
    Shows the total probability of failure up to a certain age. For example, a CDF value of 0.75 at 5 years means there's a 75% chance of failure within the first 5 years.
    
    #### Hazard Function (Failure Rate)
    Represents the likelihood of immediate failure for an asset that has survived up to a certain age. Useful for understanding how failure risk changes over time.
    
    #### Maximum Likelihood Estimation (MLE)
    A mathematical method that finds the most likely Weibull parameters to match your actual failure data. It's like finding the best-fitting curve through your data points.
    </details>
    """, unsafe_allow_html=True)
    
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