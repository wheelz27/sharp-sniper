import streamlit as st
import pandas as pd

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="EDGEINTEL | MULTI-VIEW", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #06090f; color: #c9d1d9; }
    .status-glow { color: #238636; font-weight: bold; }
    .no-bet-card { padding: 30px; border-radius: 12px; background: rgba(255,165,0,0.05); border: 1px solid rgba(255,165,0,0.2); text-align: center; }
</style>
""", unsafe_allow_html=True)

# --- 2. EXECUTIVE SIDEBAR ---
with st.sidebar:
    st.header("🎮 GLOBAL CONTROLS")
    min_edge = st.slider("Min Edge (pts/%)", 0.0, 5.0, 0.2)
    min_conf = st.slider("Min Confidence (%)", 50, 99, 65)
    st.divider()
    st.info("Multi-View mode is active. Use tabs to switch between theaters.")

# --- 3. THE DATA ENGINE ---
def get_tennis_data():
    # Mockup for Indian Wells Qualifiers / Dubai Finals
    return pd.DataFrame([
        {"Match": "Alcaraz vs Sinner", "Vegas": -110, "Model": -145, "Edge": 6.8, "Conf": 89, "Pred": "2-1 Sets"},
        {"Match": "Djokovic vs Medvedev", "Vegas": -200, "Model": -210, "Edge": 1.2, "Conf": 94, "Pred": "2-0 Sets"},
        {"Match": "Swiatek vs Sabalenka", "Vegas": +110, "Model": -105, "Edge": 4.5, "Conf": 81, "Pred": "2-1 Sets"}
    ])

def get_bball_data():
    return pd.DataFrame([
        {"Game": "Lakers @ Celtics", "Vegas": "-5.5", "Model": "-8.2", "Edge": 2.7, "Conf": 88, "Pred": "112-104"},
        {"Game": "Knicks @ 76ers", "Vegas": "+2.0", "Model": "-1.5", "Edge": 3.5, "Conf": 92, "Pred": "105-107"}
    ])

# --- 4. MULTI-VIEW LAYOUT (TABS) ---
st.title("📡 MULTI-VIEW INTELLIGENCE HUB")
st.markdown(f"**System Status:** <span class='status-glow'>● LIVE SCANNING</span>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🎾 TENNIS", "🏀 BASKETBALL", "⚔️ UFC"])

with tab1:
    df_tennis = get_tennis_data()
    # Filter Tennis data
    f_tennis = df_tennis[(df_tennis["Edge"] >= min_edge) & (df_tennis["Conf"] >= min_conf)]
    if not f_tennis.empty:
        st.dataframe(f_tennis, use_container_width=True, hide_index=True)
    else:
        st.warning("No Tennis snipes match filters. Lower Min Edge to view market.")

with tab2:
    df_bball = get_bball_data()
    # Filter Basketball data
    f_bball = df_bball[(df_bball["Edge"] >= min_edge) & (df_bball["Conf"] >= min_conf)]
    if not f_bball.empty:
        st.dataframe(f_bball, use_container_width=True, hide_index=True)
    else:
        st.warning("Scanning NBA/NCAAB for glitches...")

with tab3:
    st.info("UFC 312: Market opening in 48 hours. Intelligence engine on standby.")

# --- 5. THE SIDE-BY-SIDE VIEW (OPTIONAL) ---
st.divider()
st.subheader("📊 SPLIT-SCREEN RADAR")
col1, col2 = st.columns(2)
with col1:
    st.caption("Top Tennis Edge")
    st.write(get_tennis_data().iloc[0:1])
with col2:
    st.caption("Top Basketball Edge")
    st.write(get_bball_data().iloc[0:1])

st.divider()
st.link_button("🚀 JOIN THE SYNDICATE ON WHOP", "https://whop.com/YOUR_LINK", use_container_width=True)
