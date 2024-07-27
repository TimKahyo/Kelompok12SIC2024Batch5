import streamlit as st
import time
import random
import numpy as np

def show():
    st.title("ECG User Dashboard")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Info Pengguna")
        st.text_input("Nama", value="John Doe", disabled=True)
        
        st.subheader("Kontak Darurat")
        emergency_contact = st.text_input("Nomor Telepon")
        if st.button("Simpan Nomor"):
            st.success("Nomor kontak darurat berhasil disimpan!")

    with col2:
        st.subheader("Monitor Detak Jantung")
        bpm_placeholder = st.empty()
        chart_placeholder = st.empty()

        while True:
            bpm = random.randint(60, 100)
            bpm_placeholder.markdown(f"<h1 style='text-align: center; color: red;'>{bpm} BPM</h1>", unsafe_allow_html=True)

            chart_data = np.random.randn(20, 2)
            chart_placeholder.line_chart(chart_data)

            if bpm > 90:
                st.warning("Detak jantung Anda cukup tinggi. Cobalah untuk relaksasi dan ambil napas dalam-dalam.")
            elif bpm < 70:
                st.info("Detak jantung Anda rendah. Pastikan Anda cukup beristirahat dan minum air yang cukup.")

            time.sleep(1)