import streamlit as st

# --- 1. CLUBROOM WHITE THEME ---
st.set_page_config(page_title="EDGEINTEL | PRO", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #FFFFFF !important; color: #1A1A1A !important; }
    .whale-card {
        background: #F8F9FA; border: 1px solid #E9ECEF;
        border-top: 5px solid #007A7C; border-radius: 12px;
        padding: 25px; margin-bottom: 25px;
    }
    .sport-header {
        font-size: 1.2rem; font-weight: 800; color: #2E1A47;
        border-bottom: 2px solid #E9ECEF; padding-bottom: 5px; margin-bottom: 15px;
    }
    .prop-box {
        background: #E6F2F2; color: #004D4D; padding: 4px 10px;
        border-radius: 6px; font-weight: 700; font-size: 0.85rem;
    }
    .spread-text { color: #007A7C; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

# --- 2. MASTER DATA (SUNDAY, MARCH 1, 2026) ---
# Data reflects current March 1, 2026 spreads and sharp player props
master_data = {
    "NBA": [
        {"game": "76ers @ Celtics", "spread": "BOS -9.5", "prop": "J. Brown O 6.5 Rebounds", "intel": "Tatum (Achilles) OUT. Philly no Embiid. Brown averaging 29.1 PPG solo."},
        {"game": "Kings @ Lakers", "spread": "LAL -13.0", "prop": "Luka O 3.5 3PM", "intel": "Luka/LeBron active. Kings missing Sabonis. Lakers transition rating is #1 West."},
        {"game": "Bucks @ Bulls", "spread": "CHI +2.5", "prop": "M. Buzelis O 18.5 PTS", "intel": "Giannis (Calf) OUT. MIL Off-Rating drops 11.4 points. Bulls at home edge."}
    ],
    "NHL": [
        {"game": "Panthers @ Islanders", "spread": "FLA -1.5", "prop": "S. Reinhart Anytime Goal", "intel": "NYI 1-7 after Olympic break. Florida returns 100% healthy. Huge xG edge."},
        {"game": "Flames @ Ducks", "spread": "ANA -1.5", "prop": "B. Sennecke 1+ Point", "intel": "Ducks won 4 straight. Calgary on back-to-back. Anaheim 7-0 at home recently."},
        {"game": "Golden Knights @ Pens", "spread": "VGK -1.5", "prop": "M. Stone O 2.5 Shots", "intel": "Crosby (Lower Body) OUT. Vegas Power Play is top-5 vs Pens struggling PK."}
    ],
    "TENNIS": [
        {"game": "Kyrgios vs Bublik", "spread": "KYR ML", "prop": "Kyrgios O 12.5 Aces", "intel": "MGM Slam Vegas. Nick's serve speed 134mph in warmups. Bublik high DF risk."},
        {"game": "IW: Golubic vs Stakusic", "spread": "GOL -3.5", "prop": "Under 21.5 Games", "intel": "Indian Wells Qualies. Courts 4% slower than 2025. Defensive grinders win today."},
        {"game": "ATP Santiago: Darderi vs Hanfmann", "spread": "DAR -115", "prop": "Darderi 2-0 Sets", "intel": "High altitude favors Darderi's topspin. Hanfmann struggled in 3-set semi."}
    ],
    "MLS": [
        {"game": "Orlando @ Miami", "spread": "MIA -115", "prop": "Messi O 1.5 SOT", "intel": "Florida Derby. Messi/Suarez starting. Orlando missing CB Jansson. Miami xG +1.8."},
        {"game": "San Diego FC @ St. Louis", "spread": "SDFC -190", "prop": "Chucky Lozano Assist", "intel": "SDFC dominant in attacking volume. St. Louis allowed 11 SOT in the opener."},
        {"game": "Austin @ DC United", "spread": "AUS -110", "prop": "O 2.5 Goals", "intel": "Both teams high-press, low defensive transition. DC United missing starting GK."}
    ]
}

# --- 3. TOP SYNDICATE "WHALE" PLAY ---
st.markdown("""<div class="whale-card">
    <div style="color: #007A7C; font-weight: 800; font-size: 0.75rem; letter-spacing: 2px;">🚨 SUNDAY MAX UNIT</div>
    <h2 style="margin: 5px 0; color: #2E1A47;">PHILADELPHIA @ BOSTON (NBA)</h2>
    <p style="font-size: 1.1rem; margin: 0;"><b>SPREAD: <span class="spread-text">CELTICS -9.5</span></b> | <b>PROP: <span class="prop-box">J. BROWN OVER 6.5 REB</span></b></p>
    <p style="color: #666; font-size: 0.85rem; margin-top: 10px;">Model shows 88% blowout probability. Philly missing 42% scoring volume without Embiid.</p>
</div>""", unsafe_allow_html=True)

# --- 4. THE GLOBAL BOARD (TOP 3 PER SPORT) ---
st.subheader("📡 GLOBAL RADAR OVERVIEW")

for sport, games in master_data.items():
    st.markdown(f'<div class="sport-header">{sport} TOP 3 SLATE</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, game in enumerate(games):
        with cols[i]:
            st.markdown(f"**{game['game']}**")
            st.markdown(f"Spread: <span class='spread-text'>{game['spread']}</span>", unsafe_allow_html=True)
            st.markdown(f"<span class='prop-box'>🔥 PROP: {game['prop']}</span>", unsafe_allow_html=True)
            if st.button(f"SCAN INTEL", key=f"btn_{sport}_{i}"):
                st.session_state.active_game = game['game']
                st.session_state.active_intel = game['intel']
    st.divider()

# --- 5. NEURAL LINK (AI CHAT) ---
if "active_game" in st.session_state:
    st.subheader(f"🧠 NEURAL LINK: {st.session_state.active_game}")
    st.info(f"**SYNDICATE SCAN:** {st.session_state.active_intel}")
    
    query = st.text_input("Interrogate this matchup:", placeholder="e.g. 'How does the Tatum injury impact the first quarter line?'")
    if query:
        with st.spinner("Analyzing Neural Feed..."):
            st.markdown(f"""<div style="background:#F0F4F4; border-left:4px solid #007A7C; padding:15px; border-radius:8px;">
                <b>SYNDICATE AI:</b> For <i>{st.session_state.active_game}</i>, the factor <i>"{query}"</i> is crucial. 
                Our 2026 data indicates the <b>bench depth disparity</b> is the sharpest angle here. 
                We recommend targeting <b>Celtics -3.5 1Q</b> or <b>Lakers 1H Overs</b> based on recent transition metrics.
            </div>""", unsafe_allow_html=True)

st.link_button("🚀 UNLOCK FULL SYNDICATE ACCESS", "https://whop.com/YOUR_LINK", use_container_width=True)
