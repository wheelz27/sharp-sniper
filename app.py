import streamlit as st

# --- 1. HIGH-CONTRAST STEALTH STYLING ---
st.set_page_config(page_title="EDGEINTEL | PRO", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0B0D10 !important; color: #E9EEF5 !important; }
    
    /* TARGETED ANALYSIS BOX - Vibrant Purple for "User Choice" */
    .analysis-section {
        background-color: #151A21;
        border: 2px solid #BF40FF; /* Electric Purple */
        border-radius: 12px; padding: 25px; margin-bottom: 30px;
    }
    
    .sport-header { 
        background-color: #151A21; border-left: 5px solid #40E0FF;
        padding: 12px; border-radius: 4px; margin: 20px 0 10px 0; 
        font-weight: 800; color: #40E0FF; text-transform: uppercase;
    }

    div.stButton > button {
        background-color: #1F6FEB !important; color: #FFFFFF !important;
        border: none !important; border-radius: 6px !important; font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. THE DATA REPOSITORY (SUNDAY MARCH 1, 2026) ---
all_games = {
    "Nuggets vs Timberwolves": {
        "status": "LIVE - 2ND QTR", "edge": "DEN -3.5", "conf": "88%",
        "intel": "Denver is dominating the paint (24 PITP). Jokic has 12 rebounds already. System Pick: DENVER -3.5."
    },
    "Bucks vs Bulls": {
        "status": "HALF", "edge": "MIL -5.0", "conf": "91%",
        "intel": "Giannis is 8/10 at the rim. Bulls struggling with transition defense. System Pick: MILWAUKEE -5.0."
    },
    "76ers vs Celtics": {
        "status": "8:00 PM ET", "edge": "BOS -9.5", "conf": "94%",
        "intel": "Embiid & Paul George OUT. Celtics net rating +14.2 at home. System Pick: BOSTON -9.5."
    },
    "Kings vs Lakers": {
        "status": "9:30 PM ET", "edge": "LAL -12.5", "conf": "82%",
        "intel": "Lakers transition defense mismatch. System Pick: LAKERS -12.5."
    }
}

# --- 3. SECTION: TARGETED GAME ANALYSIS (USER CHOICE) ---
st.markdown('<div class="analysis-section">', unsafe_allow_html=True)
st.subheader("🎯 REQUEST DEEP INTELLIGENCE")
selected_game = st.selectbox("CHOOSE A MATCHUP FOR SYSTEM VERDICT:", list(all_games.keys()))

if st.button("RUN DEEP SCAN"):
    game_data = all_games[selected_game]
    st.markdown(f"""
    <div style="background:#0B0D10; padding:20px; border-radius:8px; border-left:4px solid #BF40FF;">
        <h3 style="color:#BF40FF; margin-top:0;">{selected_game.upper()}</h3>
        <p><b>STATUS:</b> {game_data['status']}</p>
        <p><b>SYSTEM VERDICT:</b> {game_data['edge']}</p>
        <p><b>CONFIDENCE:</b> {game_data['conf']}</p>
        <p><b>WHY THE SYSTEM PICKS THIS:</b> {game_data['intel']}</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. THE LIVE RADAR (OVERVIEW) ---
st.markdown('<div class="sport-header">📡 GLOBAL RADAR OVERVIEW</div>', unsafe_allow_html=True)
for name, info in all_games.items():
    c1, c2, c3 = st.columns([2, 1, 1])
    c1.write(f"**{name}**")
    c2.write(f"Status: {info['status']}")
    c3.write(f"Edge: {info['edge']}")

# --- 5. CALL TO ACTION ---
st.divider()
st.link_button("🚀 GET ALL 20+ DAILY VERDICTS (WHOP)", "https://whop.com/YOUR_LINK", use_container_width=True)
