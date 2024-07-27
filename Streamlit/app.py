import streamlit as st
from pages import home, user_ecg, user_emergence
from utils.auth import login

st.set_page_config(page_title="Mari: Sistem Pemantauan Kesehatan Jantung", layout="wide")

def main():
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("assets/logo.png", width=200)
            st.title("Mari: Sistem Pemantauan Kesehatan Jantung")
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["User ECG", "User Emergence"])
            
            if st.button("Login"):
                user = login(username, password, role)
                if user:
                    st.session_state.user = user
                    st.experimental_rerun()
                else:
                    st.error("Invalid credentials")
    else:
        if st.session_state.user["role"] == "User ECG":
            user_ecg.show()
        elif st.session_state.user["role"] == "User Emergence":
            user_emergence.show()

if __name__ == "__main__":
    main()