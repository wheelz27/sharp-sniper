import streamlit as st
import pandas as pd

# --- 1. SETTINGS & RADAR STYLING (BLACK-OPS THEME) ---
st.set_page_config(page_title="EDGEINTEL | HUB", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #06090f !important; color: #c9d1d9 !important; }
    .sport-header { 
        background: linear-gradient(90deg, #1f6feb, transparent); 
        padding: 12px 20px; border-radius: 8px; margin: 25px 0 10px 0; 
        font-weight: 900; letter-spacing: 2px; text-transform: uppercase; font-size: 0.9rem;
    }
    .intel-box {
        background-color: #0d1117; border: 1px solid #30363d;
        border-left: 4px solid #238636; padding: 20px; border-radius: 8px;
        margin: 10px 0; animation: fadeIn 0.4s;
    }
    .metric-label { font-size: 0.8rem; color: #8b949e; text-transform: uppercase; }
    .metric-value { font-size: 1.1rem; font-weight: bold; color: #58a6ff; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE DATA ENGINE (SUNDAY MARCH 1, 2026) ---
# Data includes the "WHY" analytics for the expanders
nba_data = [
    {"TIME": "18:00 EST", "GAME": "76ers @ Celtics", "VEGAS": "-8.5", "MODEL": "-11.2", "EDGE": "2.7", "ID": "NBA_1", 
     "WHY": "Celtics are 8-1 ATS at home vs Atlantic Division. Model detects 12% drop in Embiid's efficiency on 2nd night of B2B."},
    {"TIME": "20:30 EST", "GAME": "Knicks @ Spurs", "VEGAS": "+1.5", "MODEL": "-1.5", "EDGE": "3.0", "ID": "NBA_2",
     "WHY": "Knicks interior defense ranks #1 vs stretch-bigs. Model projects a 4-point swing due to Anunoby's defensive match on Wemby."},
]

tennis_data = [
    {"TIME": "14:00 UTC", "MATCH": "Sinner vs Alcaraz", "VEGAS": "-110", "MODEL": "-140", "EDGE": "5.4%", "ID": "TEN_1",
     "WHY": "Surface speed at Indian Wells favors Alcaraz's kick serve. Sinner showing slight fatigue in lateral movement metrics."},
    {"TIME": "16:00 UTC", "MATCH": "Djokovic vs Medvedev", "VEGAS": "-200", "MODEL": "-245", "EDGE": "4.2%", "ID": "TEN_2",
     "WHY": "Djokovic historical 92% win rate in Dubai Finals. Medvedev serve-depth has decreased 5 inches on average this week."},
]

# --- 3. RENDER HUB ---
st.title("📡 SYNDICATE MULTI-VIEW RADAR")
st.markdown("**Sunday, March 1, 2026** | <span style='color:#238636;'>● LIVE DATA SYNCED</span>", unsafe_allow_html=True)

# --- BASKETBALL SECTION ---
st.markdown('<div class="sport-header">🏀 NBA / NCAAB INTELLIGENCE</div>', unsafe_allow_html=True)
for game in nba_data:
    with st.container():
        col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
        col1.write(f"**{game['TIME']}**")
        col2.write(game['GAME'])
        col3.write(f"Edge: {game['EDGE']}")
        
        # Click to reveal analytics
        if col4.button("ANALYZE", key=game["ID"]):
            st.markdown(f"""
            <div class="intel-box">
                <h4 style="margin-top:0;">🧠 DEEP INTEL: {game['GAME']}</h4>
                <p><b>PROJECTION:</b> Fair line should be {game['MODEL']}.</p>
                <p><b>KEY ANALYTIC:</b> {game['WHY']}</p>
                <p style="color:#58a6ff; font-size:0.8rem;"><i>Confidence Score: 91% | Market Volume: High</i></p>
            </div>
            """, unsafe_allow_html=True)

# --- TENNIS SECTION ---
st.markdown('<div class="sport-header">🎾 ATP / WTA INTELLIGENCE</div>', unsafe_allow_html=True)
for match in tennis_
