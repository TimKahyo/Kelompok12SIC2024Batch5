import streamlit as st
from utils.auth import check_password
from PIL import Image
import os

def login():
    col1, col2, col3 = st.columns(3)
    with col2:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to the logo image
        logo_path = os.path.join(current_dir, '..', 'images', 'logo.png')
        
        # Check if the file exists before trying to open it
        if os.path.exists(logo_path):
            logo = Image.open(logo_path)
            st.image(logo, use_column_width=True)
        else:
            st.warning("Logo image not found. Please check the file path.")

    st.markdown(
        """
        <h1 style='text-align: center;'>
            <span style="color: #0036B9;">Mari:</span>
            <span style="color: #FFB923;">Sistem Pemantauan Kesehatan Jantung</span>
        </h1>
        """,
        unsafe_allow_html=True
    )
    
    login_container = st.container()
    with login_container:
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["User ECG", "User Emergence"])
            if st.button("Login"):
                if check_password(username, password, role):
                    st.session_state.authenticated = True
                    st.session_state.role = "ecg_user" if role == "ECG User" else "emergency"
                    st.experimental_rerun()
                else:
                    st.error("Invalid username, password, or role")