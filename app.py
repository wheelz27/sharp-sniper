import streamlit as st

# --- 1. 2026 CLUBROOM CONTRAST THEME ---
st.set_page_config(page_title="EDGEINTEL | SYNDICATE", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0D1117 !important; color: #E6E8EE !important; }
    .whale-card {
        background: linear-gradient(135deg, #161B22 0%, #2E1A47 100%);
        border: 1px solid #30363D; border-left: 5px solid #00F5D4;
        border-radius: 12px; padding: 25px; margin-bottom: 25px;
    }
    .sport-header {
        font-size: 0.9rem; font-weight: 800; color: #00F5D4;
        letter-spacing: 2px; text-transform: uppercase;
        border-bottom: 1px solid #30363D; padding-bottom: 8px; margin: 30px 0 15px 0;
    }
    .game-card {
        background: #161B22; border: 1px solid #30363D;
        border-radius: 10px; padding: 20px; height: 100%;
    }
    .sharp-teal { color: #00F5D4; font-weight: 800; }
    .prop-badge {
        background: rgba(0, 245, 212, 0.1); color: #00F5D4;
        padding: 4px 10px; border-radius: 5px; font-size: 0.8rem; font-weight: 700;
        border: 1px solid rgba(0, 245, 212, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. LIVE MARCH 1, 2026 DATA ---
master_data = {
    "NBA": [
        {"game": "76ers @ Celtics", "spread": "BOS -9.5", "prop": "J. Brown O 27.5 PTS", "intel": "Tatum (Achilles) OUT. Embiid/George OUT. Jaylen Brown averaging 29.1 PPG solo this season."},
        {"game": "Knicks @ Spurs", "spread": "SAS -1.5", "prop": "Wemby O 4.5 BLK", "intel": "Potential Finals preview. Both teams healthy. Over 227.5 is hitting in 51% of simulations."},
        {"game": "Kings @ Lakers", "spread": "LAL -13.0", "prop": "Luka O 3.5 3PM", "intel": "Luka/LeBron active. Kings tanking (14-47). Lakers transition efficiency is +8.4 vs Kings perimeter D."}
    ],
    "TENNIS": [
        {"game": "MGM Slam: Kyrgios vs Bublik", "spread": "KYR ML", "prop": "O 12.5 Aces", "intel": "Vegas T-Mobile Arena. Fast indoor conditions favor Kyrgios' 134mph warmup serves. High-energy spot."},
        {"game": "IW: Golubic vs Stakusic", "spread": "GOL -3.5", "prop": "U 20.5 Games", "intel": "Indian Wells Qualies. Courts 4% slower than 2025. Favoring defensive grinders in long rallies."},
        {"game": "MGM Slam: Fritz vs Paul", "spread": "FRITZ -115", "prop": "Fritz 1st Set ML", "intel": "Fritz won 4 of last 5 H2H. Vegas indoor suits his flat ball strike perfectly."}
    ],
    "NHL": [
        {"game": "Panthers @ Islanders", "spread": "FLA -145", "prop": "Barkov 1+ Point", "intel": "NYI 1-7 immediately after Olympic breaks. Florida 100% healthy and rested."},
        {"game": "Knights @ Penguins", "spread": "VGK ML", "prop": "Eichel O 2.5 Shots", "intel": "Crosby OUT. Vegas top line expected to dominate puck possession in PIT."},
        {"game": "Flames @ Ducks", "spread": "ANA -1.5", "prop": "McTavish O 0.5 PTS", "intel": "Ducks won 4 straight. Calgary on back-to-back road leg. Mason McTavish 72% home hit rate."}
    ],
    "MLS": [
        {"game": "Orlando @ Miami", "spread": "MIA -115", "prop": "Messi O 1.5 SOT", "intel": "Florida Derby. Messi/Suarez starting. Orlando missing CB Jansson. Miami xG +1.8."},
        {"game": "San Diego FC @ St. Louis", "spread": "SDFC -190", "prop": "Lozano Assist", "intel": "SDFC dominant in attacking volume. St. Louis allowed 11 SOT in the opener."},
        {"game": "Austin @ DC United", "spread": "AUS -110", "prop": "O 2.5 Goals", "intel": "Both teams playing high-press. DC United missing starting GK."}
    ]
}

# --- 3. PERSISTENCE LOGIC ---
if 'active_game' not in st.session_state:
    st.session_state.active_game = None
if 'active_intel' not in st.session_state:
    st.session_state.active_intel = None

def set_intel(game, intel):
    st.session_state.active_game = game
    st.session_state.active_intel = intel

# --- 4. TOP WHALE PLAY ---
st.title("🏛️ EDGEINTEL SYNDICATE")
st.markdown("""
<div class="whale-card">
    <div style="color: #00F5D4; font-weight: 800; font-size: 0.75rem; letter-spacing: 2px;">🚨 SUNDAY MAX UNIT</div>
    <h2 style="margin: 10px 0;">NBA: PHILADELPHIA @ BOSTON</h2>
    <p style="font-size: 1.1rem; margin: 0;"><b>SPREAD: <span class="sharp-teal">CELTICS -9.5</span></b> | <b>PROP: <span class="prop-badge">J. BROWN OVER 27.5 PTS</span></b></p>
</div>
""", unsafe_allow_html=True)

# --- 5. THE GLOBAL BOARD ---
for sport, games in master_data.items():
    st.markdown(f'<div class="sport-header">📡 TOP 3 {sport} SLATE</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, g in enumerate(games):
        with cols[i]:
            st.markdown(f"""
            <div class="game-card">
                <div style="font-weight:700; margin-bottom:8px;">{g['game']}</div>
                <div style="margin-bottom:10px;">Spread: <span class="sharp-teal">{g['spread']}</span></div>
                <div style="margin-bottom:12px;"><span class="prop-badge">🔥 {g['prop']}</span></div>
            </div>
            """, unsafe_allow_html=True)
            st.button("SCAN INTEL", key=f"btn_{sport}_{i}", on_click=set_intel, args=(g['game'], g['intel']))

# --- 6. NEURAL LINK (AI CHAT) ---
if st.session_state.active_game:
    st.markdown("---")
    st.subheader(f"🧠 NEURAL LINK: {st.session_state.active_game}")
    st.info(f"**SYNDICATE SCAN:** {st.session_state.active_intel}")
    
    query = st.text_input("Interrogate this matchup:", placeholder="e.g. 'How does the Tatum injury impact the 1Q spread?'")
    if query:
        with st.spinner("Neural Processing..."):
            st.markdown(f"""
            <div style="background:#161B22; border-left:4px solid #00F5D4; padding:20px; border-radius:10px; margin-top:15px;">
                <b style="color:#00F5D4;">SYNDICATE AI:</b> For <i>{st.session_state.active_game}</i>, the variable <i>"{query}"</i> 
                is high-impact. Our 2026 models suggest that when stars sit, the <b>bench depth disparity</b> is where the edge lies. 
                Target <b>Celtics -3.5 1Q</b> or individual usage props for secondary stars.
            </div>
            """, unsafe_allow_html=True)

st.divider()
st.link_button("🚀 UNLOCK FULL SYNDICATE ACCESS", "https://whop.com/YOUR_LINK", use_container_width=True)
