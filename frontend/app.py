import streamlit as st
from pages.login import login_page
from pages.user_ecg import user_ecg_page

# Konfigurasi halaman
st.set_page_config(page_title="Mari: Sistem Pemantauan Kesehatan Jantung", layout="wide")

# Main app
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()
else:
    # Sidebar
    st.sidebar.title("Navigasi")
    page = st.sidebar.radio("Pilih Halaman", ("User ECG", "Logout"))
    
    if page == "User ECG":
        user_ecg_page()
    elif page == "Logout":
        st.session_state.logged_in = False
        st.experimental_rerun()