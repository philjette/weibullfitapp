import streamlit as st

def configure_page_visibility():
    """
    Configure page visibility based on user authentication status.
    This function should be called from main.py before page rendering.
    
    Note: Authentication has been removed, so this function now
    simply ensures all basic pages are visible.
    """
    # All pages are accessible without authentication
    st.session_state.show_all_pages = True