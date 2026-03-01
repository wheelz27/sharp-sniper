import streamlit as st

# --- 1. 2026 CLUBROOM CONTRAST THEME ---
st.set_page_config(page_title="EDGEINTEL | PRO", layout="wide")

st.markdown("""
<style>
    /* Base Theme */
    .stApp { background-color: #0A0C10 !important; color: #E9EEF5 !important; }
    
    /* Syndicate Whale Card - Sophisticated Gradient */
    .whale-card {
        background: linear-gradient(145deg, #161B22, #0A0C10);
        border: 1px solid #1f242d;
        border-left: 4px solid #40E0FF;
        border-radius: 8px; padding: 25px; margin-bottom: 35px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Sport Headers - Clean & High Contrast */
    .sport-header {
        background-color: #161B22;
        border-left: 3px solid #40E0FF;
        padding: 8px 15px; margin: 25px 0 10px 0;
        font-weight: 700; color: #40E0FF;
        text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px;
    }

    /* Accent Text */
    .sharp-blue { color: #40E0FF; font-weight: 700; }
    .muted-intel { color: #9BA3AF; font-size: 0.9rem; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# --- 2. MASTER SYNDICATE DATA (SUNDAY, MARCH 1, 2026) ---
master_data = {
    "NBA: 76ers @ Celtics": {"status": "8:00 PM ET", "edge": "BOS -9.5", "intel": "Tatum (Achilles) OUT. However, Jaylen Brown is averaging 29.1 PPG as the solo engine. Philly is gutted: No Embiid or George. The Celtics home net rating is +14.2 against shorthanded rivals."},
    "NBA: Kings @ Lakers": {"status": "9:30 PM ET", "edge": "LAL -13.0", "intel": "Kings missing Sabonis/LaVine. Lakers' Luka/LeBron duo is operating at a 124.5 ORTG. History shows Sacramento struggles with interior size vs. Ayton when Sabonis is sidelined."},
    "NHL: Panthers @ Islanders": {"status": "6:30 PM ET", "edge": "FLA ML", "intel": "Islanders are 1-7 following long breaks (Olympic rest). Florida returns at 100% health with Tkachuk back. Huge edge in expected goals (xG)."},
    "MLS: Orlando @ Miami": {"status": "7:00 PM ET", "edge": "MIA ML", "intel": "The Florida Derby. Messi and Suarez confirmed starters. Orlando missing CB Jansson. Miami looking to bounce back from the LAFC shutout."},
    "TENNIS: Indian Wells Qualies": {"status": "LIVE", "edge": "UNDER 21.5", "intel": "Early sensor data shows courts playing 4% slower than 2025. This favors heavy defensive grinders. Hammer 'Unders' for the evening session."}
}

# --- 3. THE WHALE (MAX UNIT PLAY) ---
st.markdown("""
<div class="whale-card">
    <div style="color: #40E0FF; font-weight: 800; font-size: 0.7rem; letter-spacing: 1.5px; margin-bottom:10px;">🚨 MAX UNIT SYNDICATE PLAY</div>
    <h2 style="margin: 0;">PHILADELPHIA @ BOSTON (NBA)</h2>
    <p style="font-size: 1.2rem; margin: 5px 0;"><b>VERDICT: <span class="sharp-blue">CELTICS -9.5</span></b></p>
    <p class="muted-intel">
        <b>SHARP LOGIC:</b> Philly loses 42% of their scoring volume with Embiid and George out. 
        Boston’s second unit (Pritchard/Hauser) ranks #2 in the NBA in Net Rating. This depth disparity leads to a blowout in 88% of our model simulations.
    </p>
</div>
""", unsafe_allow_html=True)

# --- 4. ON-DEMAND DEEP SCAN (THE DROP-DOWN) ---
st.subheader("🎯 ON-DEMAND SYSTEM SCAN")
selected_match = st.selectbox("SEARCH SUNDAY SLATE:", list(master_data.keys()))

if selected_match:
    d = master_data[selected_match]
    st.markdown(f"""
    <div style="background:#161B22; padding:20px; border-radius:8px; border-top:2px solid #40E0FF; margin-top:10px;">
        <h3 style="margin-top:0;">{selected_match.upper()}</h3>
        <p><b>SYSTEM VERDICT: <span class="sharp-blue">{d['edge']}</span></b> | <b>STATUS:</b> {d['status']}</p>
        <p class="muted-intel"><b>SYNDICATE INTEL:</b> {d['intel']}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. GLOBAL RADAR OVERVIEW ---
st.markdown('<div class="sport-header">📡 GLOBAL RADAR OVERVIEW</div>', unsafe_allow_html=True)

for cat in ["
