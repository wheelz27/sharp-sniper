import streamlit as st
import pandas as pd
import random
import json
from datetime import datetime, timezone

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="EDGEINTEL | COMMAND CENTER", layout="wide")

# --- 2. CINEMATIC UI STYLING ---
st.markdown("""
<style>
.stApp {
    background: radial-gradient(1100px 600px at 12% 0%, rgba(31,111,235,0.26), rgba(0,0,0,0)),
                radial-gradient(900px 500px at 85% 10%, rgba(35,134,54,0.18), rgba(0,0,0,0)), #06090f;
    color:#c9d1d9;
}
.hero { 
    border-radius: 24px; padding: 26px; 
    background: linear-gradient(135deg, rgba(31,111,235,0.30), rgba(13,17,23,0.70)); 
    border: 1px solid rgba(255,255,255,0.08); margin-bottom: 20px;
}
.pulse {
    display: inline-block; width: 10px; height: 10px; border-radius: 50%;
    background: #238636; animation: ping 1.2s infinite; margin-right: 8px;
}
@keyframes ping { 0% { box-shadow: 0 0 0 0 rgba(35,134,54,0.7); } 70% { box-shadow: 0 0 0 10px rgba(35,134,54,0); } 100% { box-shadow: 0 0 0 0 rgba(35,134,54,0); } }
</style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("### 🎮 EXECUTIVE CONTROLS")
    theater = st.selectbox("ACTIVE THEATER", ["NBA", "NCAAB", "UFC"]) # FIX: Added sport switcher
    exec_mode = st.toggle("DEMO MODE (Force Data)", value=True)
    raiders_mode = st.toggle("☠️ Raiders Nation Badge", value=True)
    st.divider()
    min_edge = st.slider("Min Edge (pts)", 0.0, 5.0, 1.5)
    min_conf = st.slider("Min Confidence (%)", 50, 99, 85)

# --- 4. DATA ENGINE (FIXED: SWITCHES FROM UFC TO B-BALL) ---
def get_live_data(mode, sport):
    if mode and sport == "UFC":
        return pd.DataFrame([
            {"Game":"UFC 280: Makhachev vs Oliveira", "Vegas":-170, "Model":-200, "Edge":30, "Conf":92, "Tier
