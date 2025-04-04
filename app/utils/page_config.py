import streamlit as st

def configure_page_visibility():
    """
    Configure page visibility based on user authentication status.
    This function should be called from main.py before page rendering.
    """
    # If user is authenticated, ensure all pages are visible
    if st.session_state.get("user_id"):
        st.session_state.show_all_pages = True
    # If user is guest, hide login-only pages
    elif st.session_state.get("is_guest"):
        st.session_state.show_all_pages = False
    # If not authenticated at all, don't show any pages
    else:
        st.session_state.show_all_pages = False