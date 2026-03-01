import streamlit as st

# --- 1. SETTINGS & STEALTH STYLING ---
st.set_page_config(page_title="EDGEINTEL | HUB", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #06090f !important; color: #c9d1d9 !important; }
    .sport-header { 
        background: linear-gradient(90deg, #1f6feb, transparent); 
        padding: 12px 20px; border-radius: 8px; margin: 25px 0 10px 0; 
        font-weight: 900; letter-spacing: 2px; text-transform: uppercase; font-size: 0.8rem;
    }
    /* GHOST BUTTONS (NO WHITE) */
    div.stButton > button {
        background-color: transparent !important; color: #58a6ff !important;
        border: 1px solid #30363d !important; border-radius: 4px !important;
        width: 100% !important; transition: all 0.3s ease !important;
        font-size: 0.7rem !important; font-weight: bold !important;
    }
    div.stButton > button:hover {
        border-color: #1f6feb !important; background-color: rgba(31, 111, 235, 0.1) !important;
        color: white !important; box-shadow: 0 0 10px rgba(31, 111, 235, 0.4);
    }
    .intel-box {
        background-color: #0d1117; border: 1px solid #30363d;
        border-left: 4px solid #238636; padding: 20px; border-radius: 8px; margin: 10px 0;
    }
    .live-tag { color: #f85149; font-weight: bold; font-size: 0.7rem; }
</style>
""", unsafe_allow_html=True)

# --- 2. LIVE DATA HUB (MARCH 1, 2026) ---
nba_games = [
    {"TIME": "FINAL", "GAME": "Spurs @ Knicks", "SCORE": "89 - 114", "EDGE": "🎯 HIT", "ID": "NBA_1", "WHY": "Model projected a 15+ defensive swing. NYK stifled Wemby (22 turnovers caused)."},
    {"TIME": "8:00 PM", "GAME": "76ers @ Celtics", "SCORE": "0 - 0", "EDGE": "2.3", "ID": "NBA_2", "WHY": "Celtics 39-20 record vs 76ers 33-26. Efficiency edge on home court."},
]

prop_snipes = [
    {"PLAYER": "Luka Doncic", "PROP": "O 9.5 1Q PTS", "ODDS": "-115", "EDGE": "5-Star", "ID": "PROP_1", "WHY": "Luka averages 11.7 1Q points. Kings rank 28th in defensive rating."},
    {"PLAYER": "Jarrett Allen", "PROP": "O 16.5 PTS", "ODDS": "-130", "EDGE": "A- Grade", "ID": "PROP_2", "WHY": "Facing Nets defense allowing 5th most points in the paint per game."},
]

# --- 3. RENDER HUB ---
st.title("📡 SYNDICATE COMMAND CENTER")
st.caption("Sunday, March 1, 2026 | System Status: Active")

# --- NBA SECTION ---
st.markdown('<div class="sport-header">🏀 NBA LIVE BOARD</div>', unsafe_allow_html=True)
for g in nba_games:
    c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
    c1.markdown(f"<span class='live-tag'>{g['TIME']}</span>", unsafe_allow_html=True)
    c2.write(f"**{g['GAME']}** ({g['SCORE']})")
    c3.write(f"Edge: {g['EDGE']}")
    if c4.button("ANALYZE", key=g["ID"]):
        st.info(f"🧠 {g['WHY']}")

# --- PROP SNIPER SECTION ---
st.markdown('<div class="sport-header">🎯 PROP SNIPER (HIGH CONFIDENCE)</div>', unsafe_allow_html=True)
for p in prop_snipes:
    c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
    c1.write("PROJECTION")
    c2.write(f"**{
