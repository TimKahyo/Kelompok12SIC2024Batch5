import streamlit as st

def show():
    st.title("Welcome to Mari: Sistem Pemantauan Kesehatan Jantung")
    st.write(f"Hello, {st.session_state.user['username']}!")
    st.write("Please select an option from the sidebar.")