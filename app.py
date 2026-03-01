import streamlit as st

# --- 1. THEME CONFIG ---
st.set_page_config(page_title="EDGEINTEL | GLOBAL", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0B0D10 !important; color: #E9EEF5 !important; }
    .whale-section { background: linear-gradient(145deg, #1C2128, #0B0D10); border: 2px solid #FFD700; border-radius: 15px; padding: 25px; margin-bottom: 30px; }
    .request-section { background-color: #151A21; border: 2px solid #BF40FF; border-radius: 12px; padding: 25px; margin-bottom: 30px; }
    .sport-header { background-color: #151A21; border-left: 5px solid #40E0FF; padding: 10px 15px; margin: 25px 0 10px 0; font-weight: 800; color: #40E0FF; text-transform: uppercase; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE TOTAL SUNDAY BOARD (MARCH 1, 2026) ---
master_data = {
    # NBA SLATE
    "NBA: Spurs @ Knicks": {"status": "FINAL", "edge": "NYK -12.5", "conf": "WIN", "intel": "Knicks dominated the glass. Final: 114-89."},
    "NBA: Wolves @ Nuggets": {"status": "LIVE (HALF)", "edge": "MIN +8.5", "conf": "88%", "intel": "Wolves lead 58-50. Anthony Edwards attacking the drop coverage. System likes MIN to cover the adjusted live line."},
    "NBA: Bucks @ Bulls": {"status": "LIVE (Q3)", "edge": "MIL -11.5", "conf": "91%", "intel": "Bucks lead 71-60. Giannis has 24 points. Transition defense mismatch is playing out exactly as projected."},
    "NBA: Cavs @ Nets": {"status": "LIVE (HALF)", "edge": "CLE ML", "conf": "82%", "intel": "Nets lead 52-46. Cavs shooting poorly (22% 3PT); model expects a second-half correction."},
    "NBA: 76ers @ Celtics": {"status": "8:00 PM ET", "edge": "BOS -9.5", "conf": "94%", "intel": "Embiid/George OUT. Boston is 39-20 and historically dominant at TD Garden against shorthanded rivals."},
    "NBA: Kings @ Lakers": {"status": "9:30 PM ET", "edge": "LAL -13.0", "conf": "85%", "intel": "Kings managing fatigue; Lakers transition offense is #1 in the league this month. Verdict: LAKERS -13.0."},

    # NHL SLATE
    "NHL: Knights @ Penguins": {"status": "FINAL", "edge": "PIT ML", "conf": "WIN", "intel": "Penguins shutout Knights 2-0. Masterful performance on 'Mister Rogers Neighborhood Day'."},
    "NHL: Jets @ Sharks": {"status": "LIVE (P2)", "edge": "WPG ML", "conf": "89%", "intel": "Jets lead 1-0. Sharks struggling with neutral zone turnovers."},
    "NHL: Panthers @ Islanders": {"status": "6:30 PM ET", "edge": "FLA ML", "conf": "86%", "intel": "Florida's first game since the Olympic break; Islanders PK unit is currently bottom-10."},

    # MLS SLATE
    "MLS: Union @ NYCFC": {"status": "LIVE", "edge": "DRAW", "conf": "75%", "intel": "Scoreless at Subaru Park. High-pressure defensive duel."},
    "MLS: Orlando @ Inter Miami": {"status": "7:00 PM ET", "edge": "MIA ML", "conf": "83%", "intel": "Messi and Suarez both in the starting XI. Orlando missing a key center-back."},

    # TENNIS SLATE
    "TENNIS: Austin Final": {"status": "FINAL", "edge": "STEARNS ML", "conf": "WIN", "intel": "Peyton Stearns def. Townsend 7-6, 7-5. Home-court advantage for the UT Alum proved vital."},
    "TENNIS: Indian Wells Qualies": {"status": "LIVE", "edge": "GRINDERS", "conf": "88%", "intel": "Court speed is 4% slower than 2025 avg. Tail defensive specialists (Rakhimova and Timofeeva already advanced)."}
}

# --- 3. WHALE PICK ---
st.markdown("""
<div class="whale-section">
    <div style="color:#FFD700; font-weight:900; letter-spacing:2px;">🚨 SYNDICATE WHALE PICK</div>
    <h2 style="margin:10px 0;">PHILADELPHIA @ BOSTON (NBA)</h2>
    <p style="font-size:1.1rem; color:#FFFFFF;"><b>THE PICK: BOSTON CELTICS -9.5</b></p>
    <p style="color:#ADB5BD;">A 94% confidence rating with Philly's stars sidelined. This is our primary 'Max Unit' play for the night slate.</p>
</div>
""", unsafe_allow_html=True)

# --- 4. GLOBAL RADAR OVERVIEW (ALL TEAMS) ---
st.markdown('<div class="sport-header">📡 GLOBAL RADAR OVERVIEW</div>', unsafe_allow_html=True)

# Loop through categories to display all teams identically
for cat in ["NBA", "NHL", "MLS", "TENNIS"]:
    st.write(f"#### {cat} SUNDAY SLATE")
    for game, info in master_data.items():
        if game.startswith(cat):
            c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
            c1.markdown(f"**{game.split(': ')[1]}**")
            c2.write(f"{info['status']}")
            c3.write(f"Edge: **{info['edge']}**")
            if c4.button("INTEL", key=game):
                st.info(f"🧠 {info['intel']}")
    st.divider()

st.link_button("🚀 FULL SYNDICATE ACCESS (WHOP)", "https://whop.com/YOUR_LINK", use_container_width=True)
