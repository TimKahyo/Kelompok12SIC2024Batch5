import streamlit as st
import random
from utils.functions import get_ecg_history

def user_ecg_page():
    st.title(f"Selamat datang, {st.session_state.username}")
    
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        with open("assets/style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
        bpm = random.randint(60, 100)
        st.markdown(f'<div class="bpm-circle">{bpm}</div>', unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>BPM</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("Riwayat Pemantauan")
    
    history = get_ecg_history()
    
    for item in history:
        st.write(f"Tanggal: {item['tanggal']}, BPM: {item['bpm']}")