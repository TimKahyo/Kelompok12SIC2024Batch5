import streamlit as st
from PIL import Image

def login_page():
    col1, col2, col3 = st.columns(3)
    with col2:
        logo = Image.open('Streamlit/assets/logo.png')
        st.image(logo, use_column_width=True)

    st.markdown(
        """
        <h1 style='text-align: center;'>
            <span style="color: #0036B9;">Mari:</span>
            <span style="color: #FFB923;">Sistem Pemantauan Kesehatan Jantung</span>
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.subheader("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if username == "user" and password == "password":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Username atau password salah")