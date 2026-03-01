import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. SETTINGS & SYNDICATE STYLING ---
st.set_page_config(page_title="EDGEINTEL", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #06090f; color: #c9d1d9; }
    .hero { border-radius: 20px; padding: 25px; background: linear-gradient(135deg, #1f6feb, #0d1117); border: 1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

# --- 2. EXECUTIVE SIDEBAR ---
with st.sidebar:
    st.header("🎮 EXECUTIVE CONTROLS")
    theater = st.selectbox("ACTIVE THEATER", ["NBA", "NCAAB", "UFC"])
    exec_mode = st.toggle("DEMO MODE (Force Data)", value=False)
    st.divider()
    min_edge = st.slider("Min Edge (pts)", 0.0, 5.0, 0.5) # Lowered default to show more data
    min_conf = st.slider("Min Confidence (%)", 50, 99, 65)

# --- 3. DATA ENGINE ---
def get_data(mode, sport):
    if mode: # Demo Data for UFC
        return pd.DataFrame([
            {"Game":"UFC 280: Makhachev vs Oliveira", "Vegas":-170, "Model":-200, "Edge":3.0, "Conf":92},
            {"Game":"UFC 281: Adesanya vs Pereira", "Vegas":-145, "Model":-120, "Edge":2.5, "Conf":88}
        ])
    else: # Real Engine for Basketball
        try:
            from engine.matchups import MatchupAnalyzer
            analyzer = MatchupAnalyzer(sport=sport.lower())
            return pd.DataFrame(analyzer.compute_all_edges())
        except:
            return pd.DataFrame([{"Game": f"Scanning {sport} Market...", "Vegas": 0, "Model": 0, "Edge": 0, "Conf": 0}])

df = get_data(exec_mode, theater)
filtered = df[df["Edge"] >= min_edge] if not df.empty else df

# --- 4. RENDER HUB ---
st.markdown(f"<div class='hero'><h1>📡 EDGEINTEL: {theater} COMMAND</h1></div>", unsafe_allow_html=True)
st.write("")
st.table(filtered if not filtered.empty else df)

# --- 5. THE FUNNEL ---
st.divider()
st.link_button("🚀 JOIN THE SYNDICATE", "https://whop.com/YOUR_LINK", use_container_width=True)
