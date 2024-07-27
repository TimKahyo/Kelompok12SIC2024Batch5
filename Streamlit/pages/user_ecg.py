import streamlit as st
import numpy as np
import plotly.graph_objs as go
from utils.ecg_processing import process_ecg_data, predict_anomaly
from utils.database import save_ecg_data, get_latest_ecg_data

def show():
    st.title("User ECG Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # ECG Graph
        ecg_data = get_latest_ecg_data()  # Get real-time data from the database
        fig = go.Figure(data=go.Scatter(y=ecg_data, mode='lines'))
        fig.update_layout(title='Real-time ECG Data', xaxis_title='Time', yaxis_title='ECG Value')
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # BPM Display
        bpm = process_ecg_data(ecg_data)
        st.markdown(f"<h1 style='text-align: center;'>BPM</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>{bpm}</h2>", unsafe_allow_html=True)
        
        # Heart Rate Status
        if bpm < 60:
            status = "Low"
            advice = "Consider increasing physical activity or consult a doctor."
        elif bpm > 100:
            status = "High"
            advice = "Try to relax and practice deep breathing. If persists, consult a doctor."
        else:
            status = "Normal"
            advice = "Keep up the good work! Maintain a healthy lifestyle."
        
        st.markdown(f"<h3 style='text-align: center;'>Status: {status}</h3>", unsafe_allow_html=True)
        st.write(f"Advice: {advice}")
        
    # Emergency Contact
    st.subheader("Emergency Contact")
    emergency_contact = st.text_input("Enter emergency contact number")
    if st.button("Save Contact"):
        # Save contact to database
        st.success("Emergency contact saved successfully!")
    
    # Anomaly Detection
    anomaly = predict_anomaly(ecg_data)
    if anomaly:
        st.warning("Anomaly detected! Sending notification to emergency contact.")
        # Send notification logic here

if __name__ == "__main__":
    show()