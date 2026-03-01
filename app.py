import streamlit as st

# --- 1. SETTINGS & ACCESSIBLE STYLING ---
st.set_page_config(page_title="EDGEINTEL | WHALE", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0B0D10 !important; color: #E9EEF5 !important; }
    
    /* WHALE SECTION - High Priority Gold/Yellow */
    .whale-section {
        background: linear-gradient(145deg, #1C2128, #0B0D10);
        border: 2px solid #FFD700;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 30px;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
    }
    .whale-header { color: #FFD700; font-weight: 900; letter-spacing: 3px; font-size: 1.2rem; }
    
    /* SPORT HEADERS */
    .sport-header { 
        background-color: #151A21; border-left: 5px solid #40E0FF;
        padding: 12px; border-radius: 4px; margin: 25px 0 10px 0; 
        font-weight: 800; color: #40E0FF; text-transform: uppercase;
    }

    /* BUTTONS */
    div.stButton > button {
        background-color: #1F6FEB !important; color: #FFFFFF !important;
        border: none !important; border-radius: 6px !important;
        width: 100% !important; font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. THE SYNDICATE WHALE PICK (DEEP ANALYSIS) ---
st.markdown("""
<div class="whale-section">
    <div class="whale-header">🚨 SYNDICATE WHALE PICK: 76ERS @ CELTICS</div>
    <hr style="border: 0.5px solid #30363d;">
    <p style="font-size: 1.1rem; color: #FFFFFF;"><b>THE PICK: CELTICS -9.5</b></p>
    <p style="font-size: 0.95rem; color: #ADB5BD;">
        <b>Deep Analytics:</b> The line opened at -4.5 but steamed to -9.5 once <b>Joel Embiid</b> (Oblique) 
        and <b>Paul George</b> (Suspension) were confirmed OUT. While public bettors fear the "backdoor cover," 
        our model shows Boston’s 2nd unit has a +14.2 net rating against Philly’s bench. 
        <br><br>
        <b>Why we are hitting this:</b> Boston is 19-9 at home and 8-2 in their last 10. Without Embiid, 
        Philly's FG% drops by 3%, and their defensive rebounding falls to bottom-5 in the league. 
        Expect Jaylen Brown (avg 29.1 PPG) to exploit the lack of rim protection early.
    </p>
    <p style="color: #FFD700; font-weight: bold;">🎯 CONFIDENCE: 94% | SYSTEM PLAY: MAX UNIT</p>
</div>
""", unsafe_allow_html=True)

# --- 3. THE REST OF THE BOARD ---
st.markdown('<div class="sport-header">🏀 NBA AFTERNOON SLATE</div>', unsafe_allow_html=True)
nba_games = [
    {"TIME": "7:45 PM", "GAME": "Kings @ Lakers", "EDGE": "3.1", "ID": "N3"},
    {"TIME": "8:30 PM", "GAME": "Bucks @ Bulls", "EDGE": "1.4", "ID": "N4"},
]

for g in nba_games:
    c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
    c1.write(g["TIME"])
    c2.write(f"**{g['GAME']}**")
    c3.write(f"Edge: {g['EDGE']}")
    if c4.button("INTEL", key=g["ID"]):
        st.info("Searching secure servers for late-breaking rotation changes...")

st.markdown('<div class="sport-header">🏀 NCAAB SUNDAY MADNESS</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
c1.write("3:45 PM")
c2.write("**#13 Michigan St @ Indiana**")
c3.write("Edge: 2.5")
if c4.button("INTEL", key="CBK1"):
    st.success("Sparty's interior defense (98th percentile) matches Indiana's post-heavy offense perfectly. Pick: MSU -2.5.")

# --- 4. THE CALL TO ACTION ---
st.divider()
st.link_button("🚀 JOIN THE PRIVATE SYNDICATE (WHOP)", "https://whop.com/YOUR_LINK", use_container_width=True)
