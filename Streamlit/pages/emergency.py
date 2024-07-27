import streamlit as st
import time
import random

def show():
    st.title("Emergency Personel Dashboard")

    st.subheader("Daftar Notifikasi")
    notification_placeholder = st.empty()

    while True:
        notifications = [
            {"name": "John Doe", "bpm": random.randint(60, 100), "status": "Normal"},
            {"name": "Jane Smith", "bpm": random.randint(90, 120), "status": "Perhatian"},
            {"name": "Bob Johnson", "bpm": random.randint(50, 70), "status": "Peringatan"},
        ]

        with notification_placeholder.container():
            for notif in notifications:
                col1, col2, col3 = st.columns([2, 1, 1])
                col1.write(f"**{notif['name']}**")
                col2.write(f"{notif['bpm']} BPM")
                if notif['status'] == "Normal":
                    col3.success(notif['status'])
                elif notif['status'] == "Perhatian":
                    col3.warning(notif['status'])
                else:
                    col3.error(notif['status'])

        time.sleep(5)