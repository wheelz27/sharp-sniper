import streamlit as st

# --- 1. PRO-TIER DESIGN (MIDNIGHT & NEON) ---
st.set_page_config(page_title="EDGEINTEL | SYNDICATE", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #05070A !important; color: #E0E0E0 !important; }
    
    /* WHALE SECTION (NEON EMERALD) */
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
    .sharp-logic { color: #8B949E; font-size: 0.9rem; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE SYNDICATE BOARD (LIVE SUNDAY, MARCH 1, 2026) ---
# Data updated with actual afternoon scores & injury reports
master_board = {
    "NBA: Wolves @ Nuggets": {"status": "LIVE (HALF)", "edge": "DEN -3.5", "intel": "Nuggets trail 50-58. Jokic (12 reb) is abusing the drop coverage. Expect a massive 3Q push at altitude. Denver 2H ML is the sharp play."},
    "NBA: Bucks @ Bulls": {"status": "LIVE (Q3)", "edge": "MIL -11.5", "intel": "Bucks lead 73-65. Giannis (24 pts) is dominant. Bulls perimeter defense is collapsing under transition pressure. Tail the Bucks spread."},
    "NBA: 76ers @ Celtics": {"status": "8:00 PM ET", "edge": "BOS -9.5", "intel": "Embiid/George OUT. Boston's net rating at home is +14.2 against shorthanded frontcourts. Lay the points before the public hammers the line."},
    "NBA: Kings @ Lakers": {"status": "9:30 PM ET", "edge": "LAL -13.0", "intel": "Kings missing Sabonis/LaVine. Lakers' Luka/LeBron duo is averaging 124.5 ORTG. This is a potential 30-point blowout."},
    "NHL: Panthers @ Islanders": {"status": "6:30 PM ET", "edge": "FLA ML", "intel": "NYI are 1-7 following long breaks. Florida is returning at 100% health. The 'Rust Factor' makes this a high-conviction ML play."},
    "MLS: Orlando vs Inter Miami": {"status": "7:00 PM ET", "edge": "MIA ML", "intel": "Messi/Suarez confirmed starters. Orlando missing Robin Jansson (CB). Miami's xG is +1.8 higher than Orlando's current defensive setup."},
    "TENNIS: Austin Final": {"status": "FINAL", "edge": "STEARNS ML", "intel": "WIN. Stearns def. Townsend 7-6, 7-5. System accurately calculated the home-court energy factor at UT."},
    "TENNIS: Indian Wells Qualies": {"status": "LIVE", "edge": "UNDER", "intel": "Track court speed (currently 4% slower than 2025). This favors defensive grinders like Rakhimova. Hammer 'Unders' for the evening session."}
}

# --- 3. THE WHALE (MAX UNIT PLAY) ---
st.markdown("""
<div class="whale-card">
    <div style="color: #00FFA3; font-weight: 800; font-size: 0.7rem; letter-spacing: 1.5px;">🚨 MAX UNIT SYNDICATE PLAY</div>
    <h2 style="margin: 10px 0;">PHILADELPHIA @ BOSTON (NBA)</h2>
    <p style="font-size: 1.2rem; margin: 0;"><b>VERDICT: <span class="neon-text">CELTICS -9.5</span></b></p>
    <p class="sharp-logic" style="margin-top: 10px;">
        <b>SHARP INTEL:</b> Philly is gutted. No Embiid, no George. Market has not fully baked in the lack of rim protection. 
        Boston's bench (Pritchard/Hauser) creates a depth disparity that usually leads to a blowout in the 2nd half. High conviction.
    </p>
</div>
""", unsafe_allow_html=True)

# --- 4. GLOBAL RADAR ---
st.subheader("📡 THE GLOBAL RADAR")

for cat in ["NBA", "NHL", "MLS", "TENNIS"]:
    st.markdown(f'<div class="sport-header">{cat} SUNDAY BOARD</div>', unsafe_allow_
                
