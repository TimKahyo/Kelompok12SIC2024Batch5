import streamlit as st
from components.login import login
from components.sidebar import sidebar
from pages import ecg_user, emergency
from utils.auth import check_password

st.set_page_config(page_title="Mari: Sistem Pemantauan Kesehatan Jantung", layout="wide")

def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.role = None

    if not st.session_state.authenticated:
        login()
    else:
        sidebar()
        if st.session_state.role == "ecg_user":
            ecg_user.show()
        elif st.session_state.role == "emergency":
            emergency.show()

if __name__ == "__main__":
    main()