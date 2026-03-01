import streamlit as st

# --- 1. SETTINGS & BLACK-OPS STYLING ---
st.set_page_config(page_title="EDGEINTEL | HUB", layout="wide")

st.markdown("""
<style>
    /* GLOBAL DARK THEME */
    .stApp { background-color: #06090f !important; color: #c9d1d9 !important; }
    
    /* SPORT HEADERS */
    .sport-header { 
        background: linear-gradient(90deg, #1f6feb, transparent); 
        padding: 10px 18px; border-radius: 4px; margin: 25px 0 10px 0; 
        font-weight: 900; letter-spacing: 2px; text-transform: uppercase; font-size: 0.75rem;
    }

    /* STEALTH BUTTONS (NO WHITE) */
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
    .live-tag { color: #f85149; font-weight: bold; font-size: 0.7rem; }
    .status-bar { font-size: 0.8rem; opacity: 0.7; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# --- 2. LIVE SUNDAY DATA (MARCH 1, 2026) ---
nba_games = [
    {"TIME": "FINAL", "GAME": "Spurs @ Knicks", "SCORE": "89 - 114", "EDGE": "🎯 WIN", "ID": "NBA_1", "WHY": "Model accurately predicted 15+ point defensive swing. NYK interior defense neutralized Wemby."},
    {"TIME": "7:00 PM ET", "GAME": "76ers @ Celtics", "SCORE": "0 - 0", "EDGE": "2.3", "ID": "NBA_2", "WHY": "Celtics 39-20 record vs 76ers 33-26. Efficiency edge on home court via rest-day advantage."},
]

prop_snipes = [
    {"PLAYER": "Luka Doncic", "PROP": "O 9.5 1Q PTS", "ODDS": "-115", "EDGE": "HIGH", "ID": "P_1", "WHY": "Luka leads NBA in 1st quarter usage (42%). Kings defensive rating ranks 28th vs P&R ball handlers."},
    {"PLAYER": "Jarrett Allen", "PROP": "O 16.5 PTS", "ODDS": "-130", "EDGE": "MED", "ID": "P_2", "WHY": "Nets interior defense allowing 54.2 PITP (Points in the Paint) over the last 5 games."},
]

# --- 3. RENDER HUB ---
st.title("📡 SYNDICATE COMMAND CENTER")
st.markdown("<div class='status-bar'>SYSTEM: OPTIMAL | DATA: MARCH 1, 2026 | LOCATION: NEVADA, US</div>", unsafe_allow_html=True)

# --- NBA SECTION ---
st.markdown('<div class="sport-header">🏀 NBA INTELLIGENCE</div>', unsafe_allow_html=True)
for g in nba_games:
    c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
    c1.markdown(f"<span class='live-tag'>{g['TIME']}</span>", unsafe_allow_html=True)
    c2.write(f"**{g['GAME']}** ({g['SCORE']})")
    c3.write(f"Edge: {g['EDGE']}")
    if c4.button("ANALYZE", key=g["ID"]):
        st.info(f"🧠 {g['WHY']}")

# --- PROP SNIPER SECTION ---
st.markdown('<div class="sport-header">🎯 PROP SNIPER RADAR</div>', unsafe_allow_html=True)
for p in prop_snipes:
    c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
    c1.write("PROJECTION")
    c2.write(f"**{p['PLAYER']}** — {p['PROP']} ({p['ODDS']})")
    c3.write(f"Edge: {p['EDGE']}")
    if c4.button("VIEW INTEL", key=p["ID"]):
        st.success(f"📈 {p['WHY']}")

# --- 4. THE DISCORD FUNNEL ---
st.divider()
st.link_button("🚀 UNLOCK FULL SYNDICATE ACCESS (WHOP)", "https://whop.com/YOUR_LINK", use_container_width=True)
