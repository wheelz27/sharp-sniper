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

# --- 2. DATA LOAD ---
master_data = {
    "NBA": [
        {"game": "76ers @ Celtics", "spread": "BOS -9.5", "prop": "J. Brown O 28.5 PTS", "intel": "No Embiid for Philly. Brown usage spikes 12% without Tatum (Achilles rest)."},
        {"game": "Kings @ Lakers", "spread": "LAL -13.0", "prop": "Luka O 10.5 AST", "intel": "Kings transition defense is bottom-3. Luka pace-up spot is elite tonight."},
        {"game": "Bucks @ Bulls", "spread": "CHI +2.5", "prop": "M. Buzelis O 1.5 BLK", "intel": "Giannis OUT. Buzelis protecting paint against a smaller Bucks rotation."}
    ],
    "TENNIS": [
        {"game": "MGM Slam: Kyrgios/Bublik", "spread": "KYR ML", "prop": "O 24.5 Aces", "intel": "Vegas Indoor. Fast conditions. Both serving over 130mph in warmups."},
        {"game": "IW: Golubic vs Stakusic", "spread": "GOL -3.5", "prop": "U 20.5 Games", "intel": "Indian Wells sensors show 4% slower court speed today. Grinders edge."},
        {"game": "ATP Santiago Final", "spread": "DAR -115", "prop": "Darderi 2-0 Sets", "intel": "High altitude favors Darderi's topspin kick-serve over Hanfmann."}
    ],
    "NHL": [
        {"game": "Panthers @ Islanders", "spread": "FLA -1.5", "prop": "Barkov 1+ Point", "intel": "NYI 1-7 immediately after Olympic breaks. Florida is 100% healthy."},
        {"game": "Flames @ Ducks", "spread": "ANA -1.5", "prop": "Zegras O 2.5 SOG", "intel": "Ducks PP at 28%. Calgary defense on a back-to-back road leg."},
        {"game": "Knights @ Penguins", "spread": "VGK ML", "prop": "Eichel O 0.5 AST", "intel": "Crosby OUT. Vegas top line expected to dominate puck possession."}
    ]
}

# --- 3. PERSISTENCE LOGIC (This fixes the 'Intel' button) ---
if 'active_game' not in st.session_state:
    st.session_state.active_game = None
if 'active_intel' not in st.session_state:
    st.session_state.active_intel = None

def set_intel(game, intel):
    st.session_state.active_game = game
    st.session_state.active_intel = intel

# --- 4. TOP WHALE PLAY ---
st.title("🏛️ EDGEINTEL SYNDICATE")
st.markdown("""<div class="whale-card">
    <div style="color: #00F5D4; font-weight: 800; font-size: 0.75rem; letter-spacing: 2px;">🚨 MAX UNIT SYNDICATE PLAY</div>
    <h2 style="margin: 10px 0;">NBA: PHILADELPHIA @ BOSTON</h2>
    <p style="font-size: 1.1rem; margin: 0;"><b>SPREAD: <span class="sharp-teal">CELTICS -9.5</span></b> | <b>PROP: <span class="prop-badge">J. BROWN OVER 28.5 PTS</span></b></p>
</div>""", unsafe_allow_html=True)

# --- 5. GLOBAL BOARD ---
for sport, games in master_data.items():
    st.markdown(f'<div class="sport-header">📡 TOP 3 {sport} SLATE</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, g in enumerate(games):
        with cols[i]:
            st.markdown(f"""<div class="game-card">
                <div style="font-weight:700; margin-bottom:8px;">{g['game']}</div>
                <div style="margin-bottom:10px;">Spread: <span class="sharp-teal">{g['spread']}</span></div>
                <div style="margin-bottom:12px;"><span class="prop-badge">🔥 {g['prop']}</span></div>
            </div>""", unsafe_allow_html=True)
            # Use on_click callback to ensure the data sticks
            st.button("SCAN INTEL", key=f"btn_{sport}_{i}", on_click=set_intel, args=(g['game'], g['intel']))

# --- 6. NEURAL LINK (AI INTERROGATION) ---
if st.session_state.active_game:
