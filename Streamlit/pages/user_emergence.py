import streamlit as st
from utils.database import get_ecg_users, get_user_ecg_data

def show():
    st.title("User Emergence Dashboard")
    
    ecg_users = get_ecg_users()
    selected_user = st.selectbox("Select ECG User", ecg_users)
    
    if selected_user:
        user_data = get_user_ecg_data(selected_user)
        
        st.subheader(f"ECG Data for {selected_user}")
        st.line_chart(user_data["ecg_data"])
        
        st.subheader("User Information")
        st.write(f"BPM: {user_data['bpm']}")
        st.write(f"Status: {user_data['status']}")
        
        if user_data['status'] != "Normal":
            st.warning(f"Anomaly detected for {selected_user}!")
            if st.button("Contact User"):
                # Implement contact logic here
                st.success(f"Contacting {selected_user}...")

if __name__ == "__main__":
    show()