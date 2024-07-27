import streamlit as st

def sidebar():
    with st.sidebar:
        st.title("Menu")
        st.page_link("app.py", label="Home", icon="🏠")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.role = None
            st.experimental_rerun()