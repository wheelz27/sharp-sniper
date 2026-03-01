import streamlit as st

# --- 1. THEME CONFIG ---
st.set_page_config(page_title="EDGEINTEL | GLOBAL", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0B0D10 !important; color: #E9EEF5 !important; }
    .whale-section { background: linear-gradient(145deg, #1C2128, #0B0D10); border: 2px solid #FFD700; border-radius: 15px; padding: 25px; margin-bottom: 30px; }
    .request-section { background-color: #151A21; border: 2px solid #BF40FF; border-radius: 12px; padding: 25px; margin-bottom: 30px; }
    .sport-header { background-color: #151A21; border-left: 5px solid #40E0FF; padding: 10px 15px; margin: 25px 0 10px 0; font-weight: 800; color: #40E0FF; text-transform: uppercase; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE COMPLETE SUNDAY RADAR REPOSITORY (MARCH 1, 2026) ---
master_data = {
    # TENNIS SLATE
    "TENNIS: WTA Austin Final (Stearns vs Townsend)": {"status": "FINAL", "edge": "🎯 WIN", "conf": "100%", "intel": "Peyton Stearns def. Townsend 7-6, 7-5. System accurately picked the home-court advantage for the UT Alum."},
    "TENNIS: Mérida Open Final": {"status": "7:00 PM ET", "edge": "OVER 21.5", "conf": "82%", "intel": "High humidity in Mérida slows down the ball. Expect long rallies and a 3-set struggle between Bucsa and Frech."},
    "TENNIS: Indian Wells (W) Qualies": {"status": "LIVE", "edge": "LIVE VALUE", "conf": "85%", "intel": "Kamilla Rakhimova just secured her match 6-2, 6-2. Court speed is confirmed 4% slower than 2025. Tail defensive grinders in upcoming rounds."},
    
    # NBA SLATE
    "NBA: 76ers @ Celtics": {"status": "8:00 PM ET", "edge": "BOS -9.5", "conf": "94%", "intel": "Embiid/George OUT. Boston's net rating at home is +14.2 against shorthanded frontcourts."},
    "NBA: Kings @ Lakers": {"status": "9:30 PM ET", "edge": "LAL -13.5", "conf": "82%", "intel": "Kings managing heavy rotation fatigue. Lakers projected to dominate transition scoring."},
    
    # NHL & MLS
    "NHL: Panthers @ Islanders": {"status": "6:30 PM ET", "edge": "FLA ML", "conf": "85%", "intel": "Florida 1st game since break. Islanders PK unit is bottom-10 in the league currently."},
    "MLS: Orlando vs Inter Miami": {"status": "7:00 PM ET", "edge": "MIA ML", "conf": "78%", "intel": "Messi/Suarez starting. Orlando defense is missing two starters due to injury/suspension."}
}

# --- 3. THE WHALE PICK ---
st.markdown("""
<div class="whale-section">
    <div style="color:#FFD700; font-weight:900; letter-spacing:2px;">🚨 SYNDICATE WHALE PICK</div>
    <h2 style="margin:10px 0;">76ERS @ CELTICS (NBA)</h2>
    <p style="font-size:1.1rem; color:#FFFFFF;"><b>THE PICK: BOSTON CELTICS -9.5</b></p>
    <p style="color:#ADB5BD;">Philly is walking into a buzzsaw tonight. No Embiid means zero rim protection against Jaylen Brown. This is our highest confidence play for Sunday night.</p>
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

categories = ["TENNIS", "NBA", "NHL", "MLS"]
for cat in categories:
    st.write(f"--- **{cat} SLATE** ---")
    for game, info in master_data.items():
        if game.startswith(cat):
            c1, c2, c3 = st.columns([2, 1, 1])
            c1.write(f"**{game.split(': ')[1]}**")
            c2.write(f"Status: {info['status']}")
            c3.write(f"Edge: {info['edge']}")

st.divider()
st.link_button("🚀 JOIN THE PRIVATE SYNDICATE (WHOP)", "https://whop.com/YOUR_LINK", use_container_width=True)
