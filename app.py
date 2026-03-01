import streamlit as st

# --- 1. PRO-TIER STYLING (ONYX & NEON EMERALD) ---
st.set_page_config(page_title="EDGEINTEL SYNDICATE", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #05070A !important; color: #E0E0E0 !important; }
    .whale-card {
        background: linear-gradient(135deg, #0D1117 0%, #05070A 100%);
        border-left: 5px solid #00FFA3; border-radius: 4px;
        padding: 25px; margin-bottom: 30px; border-top: 1px solid #1A1D23;
    }
    .sport-header {
        color: #00FFA3; font-weight: 800; font-size: 0.75rem;
        letter-spacing: 2px; text-transform: uppercase;
        border-bottom: 1px solid #1A1D23; padding-bottom: 5px; margin-top: 25px;
    }
    .neon-text { color: #00FFA3; font-weight: bold; }
    .status-badge { background: #1A1D23; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; color: #58A6FF; }
</style>
""", unsafe_allow_html=True)

# --- 2. MASTER SYNDICATE DATA (MARCH 1, 2026) ---
master_data = {
    "NBA: 76ers @ Celtics": {"status": "8:00 PM ET", "edge": "BOS -9.5", "intel": "Philly is missing 42% of its scoring with Embiid/George out. Boston's bench is #2 in Net Rating. Blowout expected."},
    "NBA: Kings @ Lakers": {"status": "9:30 PM ET", "edge": "LAL -12.5", "intel": "Kings in tank mode. Lakers' Doncic/LeBron/Ayton trio is fully healthy. Sacramento perimeter D is bottom-3."},
    "NBA: Pelicans @ Clippers": {"status": "9:00 PM ET", "edge": "LAC -4.0", "intel": "Zion (Hamstring) is a game-time decision. Clippers have won 6 straight at the Intuit Dome."},
    "NHL: Panthers @ Islanders": {"status": "6:30 PM ET", "edge": "FLA ML", "intel": "Islanders are 1-7 in home openers after long breaks. Florida is returning with a clean injury report."},
    "NHL: Flames @ Ducks": {"status": "8:00 PM ET", "edge": "OVER 6.0", "intel": "Both teams rank bottom-5 in save percentage this month. Expect a high-scoring transition game."},
    "MLS: Orlando @ Miami": {"status": "7:00 PM ET", "edge": "MIA ML", "intel": "Messi/Suarez starting. Orlando missing key CB Jansson. Miami xG is +1.8 higher than Orlando's defense."},
    "MLS: Austin FC @ D.C. United": {"status": "9:30 PM ET", "edge": "DRAW", "intel": "Both teams playing defensive shells in the opener. Low-event game expected at Audi Field."},
    "TENNIS: Indian Wells Qualies": {"status": "LIVE", "edge": "UNDER", "intel": "Court speed is 4% slower than 2025. Favors grinders; hammer 'Unders' for the night session."}
}

# --- 3. THE WHALE (MAX UNIT) ---
st.markdown("""
<div class="whale-card">
    <div style="color: #00FFA3; font-weight: 800; font-size: 0.7rem; letter-spacing: 1.5px;">🚨 MAX UNIT SYNDICATE PLAY</div>
    <h2 style="margin: 10px 0;">PHILADELPHIA @ BOSTON (NBA)</h2>
    <p style="font-size: 1.2rem; margin: 0;"><b>VERDICT: <span class="neon-text">CELTICS -9.5</span></b></p>
    <p style="color: #8B949E; font-size: 0.9rem; margin-top: 10px;">
        <b>SHARP INTEL:</b> Embiid and George are OUT. Jaylen Brown is averaging 29.1 PPG in games where Tatum is sidelined. 
        Total mismatch in transition volume. High conviction play.
    </p>
</div>
""", unsafe_allow_html=True)

# --- 4. THE DROP-DOWN (ON-DEMAND SCAN) ---
st.subheader("🎯 ON-DEMAND SYSTEM SCAN")
# This creates the drop-down menu you asked for
selected_match = st.selectbox("SEARCH ALL SUNDAY MATCHUPS:", list(master_data.keys()))

if selected_match:
    d = master_data[selected_match]
    st.markdown(f"""
    <div style="background:#0D1117; padding:20px; border-radius:4px; border-left:4px solid #00FFA3; margin-top:10px;">
        <h3 style="margin-top:0;">{selected_match.upper()}</h3>
        <p><b>VERDICT: <span class="neon-text">{d['edge']}</span></b> | <b>STATUS:</b> {d['status']}</p>
        <p style="color:#8B949E;"><b>SYNDICATE INTEL:</b> {d['intel']}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. GLOBAL RADAR OVERVIEW ---
st.markdown('<div class="sport-header">📡 GLOBAL RADAR (SUNDAY, MARCH 1)</div>', unsafe_allow_html=True)

for cat in ["NBA", "NHL", "MLS", "TENNIS"]:
    st.write(f"#### {cat} SLATE")
    for game, info in master_data.items():
        if game.startswith(cat):
            c1, c2, c3 = st.columns([2, 1, 1])
            c1.markdown(f"**{game.split(': ')[1]}**")
            c2.write(f"{info['status']}")
            c3.markdown(f"<span class='neon-text'>{info['edge']}</span>", unsafe_allow_html=True)
    st.divider()

st.link_button("🚀 UNLOCK FULL SYNDICATE ACCESS", "
