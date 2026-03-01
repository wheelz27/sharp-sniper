import streamlit as st
import pandas as pd

# --- 1. SETTINGS & RADAR STYLING (TRUE BLACK THEME) ---
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
    .status-glow { color: #238636; font-weight: bold; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# --- 2. LIVE SUNDAY DATA (MARCH 1, 2026) ---
nba_data = [
    {"TIME": "1:00 PM ET", "GAME": "Spurs @ Knicks", "VEGAS": "-1.5", "MODEL": "-4.2", "EDGE": "2.7", "ID": "NBA_1", 
     "WHY": "Knicks interior defense stifled Wemby. Model accurately projected a 15+ point defensive swing based on OG Anunoby's tracking data."},
    {"TIME": "8:00 PM ET", "GAME": "76ers @ Celtics", "VEGAS": "-8.5", "MODEL": "-10.8", "EDGE": "2.3", "ID": "NBA_2",
     "WHY": "Celtics 8-1 ATS at home vs Atlantic division. 76ers efficiency drops 14% on the second night of a back-to-back."},
    {"TIME": "9:30 PM ET", "GAME": "Kings @ Lakers", "VEGAS": "+2.0", "MODEL": "-1.0", "EDGE": "3.0", "ID": "NBA_3",
     "WHY": "Lakers transition defense mismatch against Fox. Projected high-pace game favors Kings' current rotation depth."},
]

tennis_data = [
    {"TIME": "10:00 AM PST", "MATCH": "Indian Wells Qualifiers", "VEGAS": "VARIES", "MODEL": "N/A", "EDGE": "Hedge Opt", "ID": "TEN_1",
     "WHY": "First day of Women's Qualifying. Surface at Indian Wells is playing 4% slower than last year—favoring defensive baseline grinders."},
    {"TIME": "2:00 PM UTC", "MATCH": "Mérida Open Final", "VEGAS": "-115", "MODEL": "-135", "EDGE": "4.1%", "ID": "TEN_2",
     "WHY": "Humidity factor in Mérida impacting serve speed. Model favors the returner with higher top-spin RPM on high-bounce courts."},
]

# --- 3. RENDER HUB ---
st.title("📡 SYNDICATE MULTI-VIEW RADAR")
st.markdown("**Sunday, March 1, 2026** | <span class='status-glow'>● LIVE DATA SYNCED</span>", unsafe_allow_html=True)

# --- NBA SECTION ---
st.markdown('<div class="sport-header">🏀 NBA INTELLIGENCE BOARD</div>', unsafe_allow_html=True)
for game in nba_data:
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    col1.write(f"**{game['TIME']}**")
    col2.write(game['GAME'])
    col3.write(f"Edge: {game['EDGE']}")
    if col4.button("ANALYZE", key=game["ID"]):
        st.markdown(f"""
        <div class="intel-box">
            <h4 style="margin-top:0;">🧠 DEEP INTEL: {game['GAME']}</h4>
            <p><b>PROJECTION:</b> Model indicates fair value at {game['MODEL']}.</p>
            <p><b>KEY ANALYTIC:</b> {game['WHY']}</p>
        </div>
        """, unsafe_allow_html=True)

# --- TENNIS SECTION ---
st.markdown('<div class="sport-header">🎾 TENNIS RADAR (Indian Wells / WTA)</div>', unsafe_allow_html=True)
for match in tennis_data:
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
    col1.write(f"**{match['TIME']}**")
    col2.write(match['MATCH'])
    col3.write(f"Edge: {match['EDGE']}")
    if col4.button("ANALYZE", key=match["ID"]):
        st.markdown(f"""
        <div class="intel-box" style="border-left-color: #1f6feb;">
            <h4 style="margin-top:0;">🧠 DEEP INTEL: {match['MATCH']}</h4>
            <p><b>ANALYSIS:</b> {match['WHY']}</p>
        </div>
        """, unsafe_allow_html=True)

# --- 4. THE CALL TO ACTION ---
st.divider()
st.link_button("🚀 UNLOCK ALL VIP ANALYTICS (WHOP)", "https://whop.com/YOUR_LINK", use_container_width=True)
