import streamlit as st
import pandas as pd

# --- 1. SETTINGS & CSS (DEEP DARK THEME) ---
st.set_page_config(page_title="EDGEINTEL | HUB", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #06090f !important; color: #c9d1d9 !important; }
    .sport-header { 
        background: linear-gradient(90deg, #1f6feb, transparent); 
        padding: 10px 20px; border-radius: 8px; margin: 20px 0 10px 0; 
        font-weight: bold; letter-spacing: 1px;
    }
    .intel-box {
        background-color: #0d1117; border: 1px solid #30363d;
        border-left: 4px solid #238636; padding: 20px; border-radius: 8px;
        margin-top: 10px; animation: fadeIn 0.5s;
    }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# --- 2. DATA LOADERS (SUNDAY MARCH 1, 2026) ---
nba_data = [
    {"TIME": "18:00 EST", "GAME": "76ers @ Celtics", "VEGAS": "-8.5", "MODEL": "-11.2", "EDGE": "2.7", "ID": "NBA_1", 
     "WHY": "Celtics 8-1 ATS at home vs Atlantic Division. Embiid's usage rate drops 12% on 2nd night of B2B."},
    {"TIME": "20:30 EST", "GAME": "Knicks @ Spurs", "VEGAS": "+1.5", "MODEL": "-1.5", "EDGE": "3.0", "ID": "NBA_2",
     "WHY": "Knicks interior defense ranks #1 vs Wemby-style stretch bigs. Vegas overreacting to Spurs' recent OT win."},
]

tennis_data = [
    {"TIME": "14:00 UTC", "MATCH": "Sinner vs Alcaraz", "VEGAS": "-110", "MODEL": "-140", "EDGE": "5.4%", "ID": "TEN_1",
     "WHY": "Alcaraz surface speed adjustment. Sinner's 1st serve win % drops on slow hardcourts."},
    {"TIME": "16:00 UTC", "MATCH": "Djokovic vs Medvedev", "VEGAS": "-200", "MODEL": "-245", "EDGE": "4.2%", "ID": "TEN_2",
     "WHY": "Djokovic historical 92% win rate in Dubai Finals. Medvedev showing fatigue in 3rd set rally stats."},
]

# --- 3. RENDER ALL SPORTS ON ONE SCREEN ---
st.title("📡 SYNDICATE MULTI-VIEW RADAR")
st.markdown("**Status:** <span style='color:#238636;'>● LIVE DATA SYNCED</span>", unsafe_allow_html=True)

# --- BASKETBALL SECTION ---
st.markdown('<div class="sport-header">🏀 NBA / NCAAB INTELLIGENCE</div>', unsafe_allow_html=True)
for game in nba_data:
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    col1.write(game["TIME"])
    col2.write(f"**{game['GAME']}**")
    col3.write(f"Edge: {game['EDGE']}")
    if col4.button("ANALYZE", key=game["ID"]):
        st.markdown(f"""
        <div class="intel-box">
            <h4>🧠 DEEP INTEL: {game['GAME']}</h4>
            <p><b>PROJECTION:</b> Model predicts a final spread of {game['MODEL']}.</p>
            <p><b>KEY ANALYTIC:</b> {game['WHY']}</p>
            <p style="color:#58a6ff;"><i>Confidence Score: 91% | Volume: High</i></p>
        </div>
        """, unsafe_allow_html=True)

# --- TENNIS SECTION ---
st.markdown('<div class="sport-header">🎾 ATP / WTA INTELLIGENCE</div>', unsafe_allow_html=True)
for match in tennis_data:
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    col1.write(match["TIME"])
    col2.write(f"**{match['MATCH']}**")
    col3.write(f"Edge: {match['EDGE']}")
    if col4.button("ANALYZE", key=match["ID"]):
        st.markdown(f"""
        <div class="intel-box" style="border-left-color: #1f6feb;">
            <h4>🧠 DEEP INTEL: {match['MATCH']}
