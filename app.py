import streamlit as st

# --- 1. PRO-TIER STYLING (ONYX & NEON EMERALD) ---
st.set_page_config(page_title="EDGEINTEL PRO", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #05070A !important; color: #E0E0E0 !important; }
    
    /* SYNDICATE WHALE CARD */
    .whale-card {
        background: linear-gradient(135deg, #0D1117 0%, #05070A 100%);
        border-left: 5px solid #00FFA3;
        border-right: 1px solid #1A1D23;
        border-top: 1px solid #1A1D23;
        border-bottom: 1px solid #1A1D23;
        border-radius: 4px; padding: 25px; margin-bottom: 30px;
    }

    /* MATCHUP ROWS */
    .match-row {
        background-color: #0D1117; border: 1px solid #1A1D23;
        padding: 15px; border-radius: 4px; margin-bottom: 10px;
    }
    
    .sport-label {
        color: #00FFA3; font-weight: 800; font-size: 0.75rem;
        letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 5px;
    }

    .intel-text { color: #8B949E; font-size: 0.9rem; line-height: 1.4; }
    
    /* NEON ACCENTS */
    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    .neon-text { color: #00FFA3; font-weight: bold; }
    .status-badge { background: #1A1D23; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; color: #58A6FF; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE DEEP INTELLIGENCE DATA (MARCH 1, 2026) ---
# Hard-hitting analysis based on 2026 rosters and injuries
syndicate_board = {
    "NBA: 76ers @ Celtics": {
        "status": "8:00 PM ET", "edge": "BOS -11.5", 
        "logic": "Market hasn't adjusted to Jayson Tatum (Achilles) being out vs Embiid (Oblique) also being out. This is a 'System Wash.' However, Boston's 2nd unit (Pritchard/Hauser) ranks #2 in Net Rating. Philly's bench is bottom-5. Expect Boston's depth to blow this open in the late 3rd."
    },
    "NBA: Kings @ Lakers": {
        "status": "9:30 PM ET", "edge": "LAL -13.0", 
        "logic": "Kings are a 'Dead Team Walking'—Sabonis, LaVine, and Hunter are all out post-surgery. Lakers running a Doncic/LeBron/Ayton trio. Sacramento has zero interior size to stop Ayton. High probability of a 20+ point blowout."
    },
    "NHL: Panthers @ Islanders": {
        "status": "6:30 PM ET", "edge": "FLA ML", 
        "logic": "Islanders are 1-7 in their last 8 home openers following long breaks. Florida is returning at full health. The 'Rust Factor' is heavily weighted toward a Panthers dominant win."
    },
    "MLS: Orlando vs Inter Miami": {
        "status": "7:00 PM ET", "edge": "MIA ML", 
        "logic": "Messi and Suarez confirmed starters. Orlando's Robin Jansson (Foot) is out, leaving a massive hole in their central defense. Miami's expected goals (xG) is +1.8 higher than Orlando's defensive average."
    },
    "TENNIS: Indian Wells (W) Qualies": {
        "status": "LIVE", "edge": "UNDER 20.5", 
        "logic": "Early sensor data shows court speed at Indian Wells is 4% slower than 2025. This creates massive rallies that exhaust lower-ranked qualifiers. Look for the 'Under' in matches involving heavy defensive grinders."
    }
}

# --- 3. TOP OF FOLD: THE WHALE ---
st.markdown(f"""
<div class="whale-card">
    <div class="sport-label">🚨 MAX UNIT SYNDICATE PLAY</div>
    <h2 style="margin: 5px 0;">SACRAMENTO KINGS @ LA LAKERS</h2>
    <p style="font-size: 1.2rem; margin: 0;"><b>THE VERDICT: <span class="neon-text">
