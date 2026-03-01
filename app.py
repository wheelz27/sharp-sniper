import streamlit as st

# --- 1. PRO-TIER STYLING (ONYX & NEON EMERALD) ---
st.set_page_config(page_title="EDGEINTEL SYNDICATE", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #05070A !important; color: #E0E0E0 !important; }
    
    /* SYNDICATE WHALE CARD */
    .whale-card {
        background: linear-gradient(135deg, #0D1117 0%, #05070A 100%);
        border-left: 5px solid #00FFA3; border-radius: 4px;
        padding: 25px; margin-bottom: 30px; border-top: 1px solid #1A1D23;
    }

    /* SPORT HEADERS */
    .sport-header {
        color: #00FFA3; font-weight: 800; font-size: 0.75rem;
        letter-spacing: 2px; text-transform: uppercase;
        border-bottom: 1px solid #1A1D23; padding-bottom: 5px; margin-top: 25px;
    }

    .intel-box {
        background: #0D1117; border: 1px solid #1A1D23;
        padding: 15px; border-radius: 4px; margin-top: 10px;
    }

    .neon-text { color: #00FFA3; font-weight: bold; }
    .status-badge { background: #1A1D23; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; color: #58A6FF; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE DEEP INTELLIGENCE DATA (LIVE MARCH 1, 2026) ---
master_board = {
    "NBA: Wolves @ Nuggets": {"status": "LIVE (HALF)", "edge": "DEN -3.5", "intel": "Nuggets trail 50-58. Jokic (12 reb) is abusing drop coverage. Expect a massive 3Q push at altitude. Denver 2H ML is the sharp play."},
    "NBA: Bucks @ Bulls": {"status": "LIVE (Q3)", "edge": "MIL -11.5", "intel": "Bucks lead 73-65. Giannis (24 pts) is dominant. Bulls perimeter defense is collapsing. Tail the Bucks spread."},
    "NBA: 76ers @ Celtics": {"status": "8:00 PM ET", "edge": "BOS -9.5", "intel": "Embiid/George OUT. Tatum (Achilles) also OUT. Boston's bench (Pritchard/Hauser) ranks #2 in Net Rating; Philly's is bottom-5. Depth wins this late."},
    "NBA: Kings @ Lakers": {"status": "9:30 PM ET", "edge": "LAL -13.0", "intel": "Kings missing Sabonis/LaVine. Lakers' Luka/LeBron duo is averaging 124.5 ORTG. High probability of a 20+ point blowout."},
    "NHL: Panthers @ Islanders": {"status": "6:30 PM ET", "edge": "FLA ML", "intel": "NYI are 1-7 following long breaks. Florida is at 100% health. The 'Rust Factor' makes this a high-conviction ML play."},
    "TENNIS: Austin Final": {"status": "FINAL", "edge": "STEARNS ML", "intel": "WIN. Stearns def. Townsend 7-6, 7-5. System accurately tracked the 'Home Court' energy factor for the UT Alum."},
    "MLS: Orlando vs Inter Miami": {"status": "7:00 PM ET", "edge": "MIA ML", "intel": "Messi/Suarez starting. Orlando missing Robin Jansson (CB). Miami's xG is +1.8 higher than Orlando's current setup."}
}

# --- 3. TOP OF FOLD: THE WHALE ---
st.markdown("""
<div class="whale-card">
    <div style="color: #00FFA3; font-weight: 800; font-size: 0.7rem; letter-spacing: 1.5px;">🚨 MAX UNIT SYNDICATE PLAY</div>
    <h2 style="margin: 10px 0;">PHILADELPHIA @ BOSTON (NBA)</h2>
    <p style="font-size: 1.2rem; margin: 0;"><b>VERDICT:
