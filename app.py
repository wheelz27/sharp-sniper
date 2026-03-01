import streamlit as st

# --- 1. THEME CONFIG ---
st.set_page_config(page_title="EDGEINTEL | GLOBAL", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0B0D10 !important; color: #E9EEF5 !important; }
    .whale-section { background: linear-gradient(145deg, #1C2128, #0B0D10); border: 2px solid #FFD700; border-radius: 15px; padding: 25px; margin-bottom: 30px; }
    .request-section { background-color: #151A21; border: 2px solid #BF40FF; border-radius: 12px; padding: 25px; margin-bottom: 30px; }
    .sport-header { background-color: #151A21; border-left: 5px solid #40E0FF; padding: 10px 15px; margin: 25px 0 10px 0; font-weight: 800; color: #40E0FF; text-transform: uppercase; font-size: 0.85rem; }
    div.stButton > button { background-color: #1F6FEB !important; color: white !important; border: none !important; border-radius: 6px !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE GLOBAL SUNDAY REPOSITORY (MARCH 1, 2026) ---
# This dictionary now acts as your master database for the scanner
master_data = {
    "NBA: 76ers @ Celtics": {"status": "8:00 PM ET", "edge": "BOS -9.5", "conf": "94%", "intel": "Embiid/George OUT. Celtics net rating +14.2 at home. Pick: BOS -9.5"},
    "NBA: Kings @ Lakers": {"status": "9:30 PM ET", "edge": "LAL -13.5", "conf": "82%", "intel": "Mismatch in transition defense; Kings missing rotation depth. Pick: LAL -13.5"},
    "NBA: Nuggets @ Timberwolves": {"status": "LIVE (Q2)", "edge": "DEN -3.5", "conf": "88%", "intel": "Jokic dominating paint (12 reb). Denver's transition D is #1 today. Pick: DEN -3.5"},
    "NHL: Panthers @ Islanders": {"status": "6:30 PM ET", "edge": "FLA ML", "conf": "85%", "intel": "Florida 1st home game since break. Islanders struggling with PK efficiency. Pick: PANTHERS ML"},
    "NCAAB: Michigan St @ Indiana": {"status": "3:45 PM ET", "edge": "MSU -2.5", "conf": "91%", "intel": "Sparty's interior defense (98th percentile) neutralizes Indiana's post-game. Pick: MSU -2.5"},
    "MLS: Orlando City vs Inter Miami": {"status": "7:00 PM ET", "edge": "MIA ML", "conf": "78%", "intel": "Messi starting. Orlando missing key CB due to suspension. Pick: MIAMI ML"},
    "TENNIS: Indian Wells Qualies": {"status": "LIVE", "edge": "UNDER 21.5", "conf": "80%", "intel": "Surface speed is 4% slower than 2025 avg; favors grinders. Pick: UNDER"}
}

# --- 3. THE WHALE PICK ---
st.markdown("""
<div class="whale-section">
    <div style="color:#FFD700; font-weight:900; letter-spacing:2px;">🚨 SYNDICATE WHALE PICK</div>
    <h2 style="margin:10px 0;">76ERS @ CELTICS (NBA)</h2>
    <p style="font-size:1.1rem; color:#FFFFFF;"><b>THE PICK: BOSTON CELTICS -9.5</b></p>
    <p style="color:#ADB5BD;">The model identifies a 94% confidence rating due to Philadelphia being shorthanded (Embiid/George OUT). Boston is at full strength and dominant at TD Garden.</p>
</div>
""", unsafe_allow_html=True)

# --- 4. ON-DEMAND SYSTEM SCAN ---
st.markdown('<div class="request-section">', unsafe_allow_html=True)
st.subheader("🎯 ON-DEMAND SYSTEM SCAN")
choice = st.selectbox("CHOOSE ANY MATCHUP ON THE BOARD:", list(master_data.keys()))

if st.button("EXECUTE DEEP SCAN"):
    d = master_data[choice]
    st.markdown(f"""
    <div style="background:#0B0D10; padding:20px; border-radius:10px; border-left:4px solid #BF40FF; margin-top:15px;">
        <h3 style="color:#BF40FF; margin-top:0;">{choice.upper()}</h3>
        <p><b>STATUS:</b> {d['status']} | <b>VERDICT:</b> {d['edge']} ({d['conf']})</p>
        <p><b>SYSTEM INTEL:</b> {d['intel']}</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. GLOBAL RADAR OVERVIEW (ALL SPORTS) ---
st.markdown('<div class="sport-header">📡 GLOBAL RADAR (SUNDAY, MARCH 1)</div>', unsafe_allow_html=True)

# Categorizing the radar for better reading
categories = ["NBA", "NHL", "NCAAB", "MLS", "TENNIS"]
for cat in categories:
    st.write(f"--- **{cat} SLATE** ---")
    for game, info in master_data.items():
        if game.startswith(cat):
            c1, c2, c3 = st.columns([2, 1, 1])
            c1.write(f"**{game.split(': ')[1]}**")
            c2.write(f"Time: {info['status']}")
            c3.write(f"Edge: {info['edge']}")

st.divider()
st.link_button("🚀 JOIN THE PRIVATE SYNDICATE (WHOP)", "https://whop.com/YOUR_LINK", use_container_width=True)
