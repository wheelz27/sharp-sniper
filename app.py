import streamlit as st

# --- 1. SETTINGS & ACCESSIBILITY STYLING ---
st.set_page_config(page_title="EDGEINTEL | ACCESSIBLE", layout="wide")

st.markdown("""
<style>
    /* 2026 HIGH-CONTRAST DARK THEME */
    .stApp { 
        background-color: #0B0D10 !important; /* Deep Charcoal instead of Black */
        color: #E9EEF5 !important;           /* High-contrast Off-White */
    }
    
    /* SPORT HEADERS - High Visibility Blue */
    .sport-header { 
        background-color: #151A21;
        border-left: 5px solid #40E0FF; /* Electric Cyan Accent */
        padding: 15px; 
        border-radius: 4px; 
        margin: 25px 0 10px 0; 
        font-weight: 800;
        color: #40E0FF;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* ACCESSIBLE BUTTONS (Glow Blue) */
    div.stButton > button {
        background-color: #1F6FEB !important; /* Solid Blue for visibility */
        color: #FFFFFF !important;            /* Pure White text */
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
    }
    div.stButton > button:hover {
        background-color: #40E0FF !important; /* Cyan hover for clear feedback */
        color: #0B0D10 !important;
        transform: translateY(-2px);
    }

    /* INTEL BOX - Elevated surface for depth */
    .intel-box {
        background-color: #1C2128; 
        border: 1px solid #444C56;
        padding: 25px; 
        border-radius: 12px; 
        margin: 15px 0;
        color: #ADB5BD; /* Softer grey for body text */
    }
    
    .win-tag { color: #3FB950; font-weight: 900; } /* Success Green */
    .live-tag { color: #F85149; font-weight: 900; } /* Urgent Red */
</style>
""", unsafe_allow_html=True)

# --- 2. THE DATA FEED ---
nba_games = [
    {"TIME": "FINAL", "GAME": "Spurs @ Knicks", "SCORE": "89 - 114", "EDGE": "WIN", "ID": "N1", "WHY": "Model predicted 15+ defensive swing. NYK neutralized Wemby."},
    {"TIME": "LIVE", "GAME": "76ers @ Celtics", "SCORE": "22 - 18", "EDGE": "2.3", "ID": "N2", "WHY": "Celtics showing 4% efficiency edge on home court via rest-day advantage."},
]

prop_snipes = [
    {"PLAYER": "Luka Doncic", "PROP": "O 9.5 1Q PTS", "EDGE": "HIGH", "ID": "P1", "WHY": "Luka leads NBA in 1st quarter usage (42%)."},
    {"PLAYER": "Jarrett Allen", "PROP": "O 16.5 PTS", "EDGE": "MED", "ID": "P2", "WHY": "Nets allowing 54 PITP over last 5 games."},
]

# --- 3. RENDER HUB ---
st.title("📡 SYNDICATE COMMAND CENTER")
st.markdown("<p style='opacity:0.8;'>System Status: Optimal | High Contrast Mode: ON</p>", unsafe_allow_html=True)

# --- NBA SECTION ---
st.markdown('<div class="sport-header">🏀 NBA INTELLIGENCE</div>', unsafe_allow_html=True)
for g in nba_games:
    c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
    # Use bold tags for easier reading
    status_color = "win-tag" if g["TIME"] == "FINAL" else "live-tag"
    c1.markdown(f"<span class='{status_color}'>● {g['TIME']}</span>", unsafe_allow_html=True)
    c2.markdown(f"**{g['GAME']}** <br>Score: {g['SCORE']}", unsafe_allow_html=True)
    c3.markdown(f"Edge: **{g['EDGE']}**")
    if c4.button("ANALYZE", key=g["ID"]):
        st.markdown(f"<div class='intel-box'><b>🧠 DEEP INTEL:</b><br>{g['WHY']}</div>", unsafe_allow_html=True)

# --- PROP SNIPER SECTION ---
st.markdown('<div class="sport-header">🎯 PROP SNIPER RADAR</div>', unsafe_allow_html=True)
for p in prop_snipes:
    c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
    c1.write("PROJECTION")
    c2.markdown(f"**{p['PLAYER']}** <br> {p['PROP']}")
    c3.markdown(f"Edge: **{p['EDGE']}**")
    if c4.button("VIEW INTEL", key=p["ID"]):
        st.markdown(f"<div class='intel-box'><b>📈 PROP ANALYTIC:</b><br>{p['WHY']}</div>", unsafe_allow_html=True)

# --- 4. CALL TO ACTION ---
st.divider()
st.link_button("🚀 UNLOCK FULL SYNDICATE ACCESS (WHOP)", "https://whop.com/YOUR_LINK", use_container_width=True)
