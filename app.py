import streamlit as st

# --- 1. SETTINGS & RADAR STYLING (THE "NO WHITE" FIX) ---
st.set_page_config(page_title="EDGEINTEL | HUB", layout="wide")

st.markdown("""
<style>
    /* GLOBAL DARK MODE */
    .stApp { background-color: #06090f !important; color: #c9d1d9 !important; }
    
    /* SPORT HEADERS */
    .sport-header { 
        background: linear-gradient(90deg, #1f6feb, transparent); 
        padding: 12px 20px; border-radius: 8px; margin: 25px 0 10px 0; 
        font-weight: 900; letter-spacing: 2px; text-transform: uppercase; font-size: 0.8rem;
    }

    /* THE BUTTON FIX: MISSION CRITICAL */
    div.stButton > button {
        background-color: transparent !important;
        color: #58a6ff !important;
        border: 1px solid #30363d !important;
        border-radius: 4px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        font-size: 0.7rem !important;
        font-weight: bold !important;
    }
    div.stButton > button:hover {
        border-color: #1f6feb !important;
        background-color: rgba(31, 111, 235, 0.1) !important;
        color: white !important;
        box-shadow: 0 0 10px rgba(31, 111, 235, 0.4);
    }

    /* INTEL BOX */
    .intel-box {
        background-color: #0d1117; border: 1px solid #30363d;
        border-left: 4px solid #238636; padding: 20px; border-radius: 8px;
        margin: 10px 0; animation: fadeIn 0.4s;
    }
    .live-tag { color: #f85149; font-weight: bold; font-size: 0.7rem; }
</style>
""", unsafe_allow_html=True)

# --- 2. LIVE SUNDAY DATA (MARCH 1, 2026) ---
nba_data = [
    {"TIME": "LIVE Q4", "GAME": "Spurs @ Knicks", "SCORE": "89 - 114", "EDGE": "2.7", "ID": "NBA_1", 
     "WHY": "Knicks interior defense stifled Wemby. Model accurately projected a 15+ point defensive swing."},
    {"TIME": "8:00 PM ET", "GAME": "76ers @ Celtics", "SCORE": "0 - 0", "EDGE": "2.3", "ID": "NBA_2",
     "WHY": "Celtics 8-1 ATS at home. 76ers efficiency drops on B2B road games."},
]

tennis_data = [
    {"TIME": "10:00 AM PST", "MATCH": "Indian Wells Qualies", "EDGE": "Hedge Opt", "ID": "TEN_1",
     "WHY": "Surface playing 4% slower than 2025. Favor baseline grinders in early rounds."},
    {"TIME": "2:00 PM UTC", "MATCH": "Mérida Open Final", "EDGE": "4.1%", "ID": "TEN_2",
     "WHY": "Humidity factor impacting serve speed. Model favors the returner with high-spin RPM."},
]

# --- 3. RENDER HUB ---
st.title("📡 SYNDICATE MULTI-VIEW RADAR")
st.markdown("**Sunday, March 1, 2026** | <span style='color:#238636;'>● DATA SYNCED</span>", unsafe_allow_html=True)

# --- NBA SECTION ---
st.markdown('<div class="sport-header">🏀 NBA INTELLIGENCE BOARD</div>', unsafe_allow_html=True)
for game in nba_data:
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    col1.markdown(f"<span class='live-tag'>{game['TIME']}</span>", unsafe_allow_html=True)
    col2.write(f"**{game['GAME']}** ({game['SCORE']})")
    col3.write(f"Edge: {game['EDGE']}")
    if col4.button("ANALYZE", key=game["ID"]):
        st.markdown(f"""<div class="intel-box"><h4>🧠 DEEP INTEL: {game['GAME']}</h4><p>{game['WHY']}</p></div>""", unsafe_allow_html=True)

# --- TENNIS SECTION ---
st.markdown('<div class="sport-header">🎾 TENNIS RADAR (ATP/WTA)</div>', unsafe_allow_html=True)
for match in tennis_data:
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    col1.write(game['TIME'])
    col2.write(match['MATCH'])
    col3.write(f"Edge: {match['EDGE']}")
    if col4.button("ANALYZE", key=
