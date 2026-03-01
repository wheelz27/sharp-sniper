import streamlit as st

# --- 1. THEME & ACCESSIBILITY ---
st.set_page_config(page_title="EDGEINTEL | HUB", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0B0D10 !important; color: #E9EEF5 !important; }
    
    /* WHALE BOX (GOLD) */
    .whale-section {
        background: linear-gradient(145deg, #1C2128, #0B0D10);
        border: 2px solid #FFD700; border-radius: 15px;
        padding: 25px; margin-bottom: 30px;
    }
    
    /* SCANNER BOX (PURPLE) */
    .request-section {
        background-color: #151A21; border: 2px solid #BF40FF;
        border-radius: 12px; padding: 25px; margin-bottom: 30px;
    }

    /* HEADERS & BUTTONS */
    .sport-header { 
        background-color: #151A21; border-left: 5px solid #40E0FF;
        padding: 12px; margin: 20px 0 10px 0; font-weight: 800; color: #40E0FF;
    }
    div.stButton > button {
        background-color: #1F6FEB !important; color: white !important;
        border: none !important; border-radius: 6px !important; font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. LIVE SUNDAY DATA (MARCH 1, 2026) ---
all_games = {
    "76ers @ Celtics": {
        "status": "8:00 PM ET", "edge": "BOS -9.5", "conf": "94%",
        "intel": "Joel Embiid and Paul George are officially OUT. Boston's net rating at home is +14.2 against shorthanded lineups. Jaylen Brown (29.1 PPG) is the primary engine tonight. Verdict: CELTICS -9.5."
    },
    "Kings @ Lakers": {
        "status": "9:30 PM ET", "edge": "LAL -13.0", "conf": "82%",
        "intel": "Lakers are heavy 13-point favorites. LeBron (foot) is questionable, but Luka Doncic is projected to clear 32.5 points. Verdict: LAKERS -13.0."
    },
    "Bucks @ Bulls": {
        "status": "FINAL", "edge": "MIL -15.5", "conf": "WIN",
        "intel": "Milwaukee dominated the paint early. Giannis finished with 30+. System accurately tracked the transition mismatch."
    }
}

# --- 3. SECTION: THE WHALE PICK ---
st.markdown("""
<div class="whale-section">
    <div style="color:#FFD700; font-weight:900; letter-spacing:2px;">🚨 FEATURED WHALE PICK</div>
    <h2 style="margin:10px 0;">76ERS @ CELTICS (SUN MARCH 1)</h2>
    <p style="font-size:1.1rem;"><b>THE PICK: CELTICS -9.5</b></p>
    <p style="color:#ADB5BD;">Philly is gutted tonight. No Embiid, no George. Boston is 39-22 and looking to extend their lead in the East. Our system identifies a massive rim-protection void that Jaylen Brown will exploit.</p>
</div>
""", unsafe_allow_html=True)

# --- 4. SECTION: DEEP INTELLIGENCE REQUEST ---
st.markdown('<div class="request-section">', unsafe_allow_html=True)
st.subheader("🎯 ON-DEMAND SYSTEM SCAN")
choice = st.selectbox("SELECT MATCHUP:", list(all_games.keys()))

if st.button("EXECUTE SCAN"):
    data = all_games[choice]
    st.markdown(f"""
    <div style="background:#0B0D10; padding:20px; border-radius:10px; border-left:4px solid #BF40FF; margin-top:15px;">
        <h3 style="color:#BF40FF; margin-top:0;">{choice.upper()}</h3>
        <p><b>SYSTEM VERDICT:</b> {data['edge']} ({data['conf']})</p>
        <p><b>INTEL:</b> {data['intel']}</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 5. SECTION: GLOBAL RADAR ---
st.markdown('<div class="sport-header">📡 GLOBAL RADAR OVERVIEW</div>', unsafe_allow_html=True)
for name, info in all_games.items():
    c1, c2, c3 = st.columns([2, 1, 1])
    c1.markdown(f"**{name}**")
    c2.write(info['status'])
