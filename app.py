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

# --- 2. LIVE DATA: SUNDAY, MARCH 1, 2026 ---
master_data = {
    "NBA": [
        {"game": "76ers @ Celtics", "spread": "BOS -9.5", "prop": "J. Brown O 29.5 PTS", "intel": "Tatum (Achilles) OUT. Embiid (Oblique) OUT. Jaylen Brown usage rate is 38.4% without Tatum on the floor."},
        {"game": "Bucks @ Bulls", "spread": "CHI +2.5", "prop": "M. Buzelis O 18.5 PTS", "intel": "Giannis (Calf) OUT. Milwaukee's interior defense rating drops significantly. Bulls home dog edge."},
        {"game": "Kings @ Lakers", "spread": "LAL -13.0", "prop": "Luka O 10.5 AST", "intel": "Luka/LeBron ACTIVE. Kings in full tank mode. Lakers transition efficiency is league-high tonight."}
    ],
    "TENNIS": [
        {"game": "MGM Slam: Kyrgios vs Bublik", "spread": "KYR ML", "prop": "Kyrgios O 12.5 Aces", "intel": "Vegas T-Mobile Arena. 10-point tiebreak format favors Kyrgios' high-velocity first serve (134mph in warmups)."},
        {"game": "IW: Golubic vs Stakusic", "spread": "GOL -3.5", "prop": "Under 21.5 Games", "intel": "Indian Wells sensors show courts playing 4% slower than 2025. This heavily favors Golubic’s baseline grinding."},
        {"game": "MGM Slam: Fritz vs Paul", "spread": "FRITZ ML", "prop": "Fritz 1st Set Winner", "intel": "Fritz has won 4 of last 5 head-to-heads. The Vegas indoor conditions suit his flat ball strike."}
    ],
    "NHL": [
        {"game": "Panthers @ Islanders", "spread": "FLA -1.5", "prop": "S. Reinhart Goal", "intel": "NYI are 1-7 in games immediately following the Olympic break. Florida is healthy and rested."},
        {"game": "Blackhawks @ Utah Mammoth", "spread": "UTA -350", "prop": "L. Cooley O 0.5 PTS", "intel": "Utah has 69% win probability. Cooley has recorded points in 4 of his last 5 home games."},
        {"game": "Flames @ Ducks", "spread": "ANA -1.5", "prop": "Zegras O 2.5 SOG", "intel": "Ducks are on a 4-game win streak. Calgary is playing their second leg of a back-to-back."}
    ],
    "MLS": [
        {"game": "Orlando @ Miami", "spread": "MIA -115", "prop": "Messi O 1.5 SOT", "intel": "Florida Derby. Messi/Suarez starting. Orlando missing CB Jansson. Miami seeking first goal of 2026."},
        {"game": "San Diego FC @ St. Louis", "spread": "SDFC -190", "prop": "Lozano Assist", "intel": "SDFC scored 9 goals in first 3 matches. St. Louis defense allowed 11 shots on target in their opener."},
        {"game": "Austin @ DC United", "spread": "AUS -110", "prop": "O 2.5 Goals", "intel": "Both teams playing high-press with low defensive transition. DC United missing starting GK."}
    ]
}

# --- 3. SESSION STATE FOR INTEL ---
if 'active_game' not in st.session_state:
    st.session_state.active_game = None
if 'active_intel' not in st.session_state:
    st.session_state.active_intel = None

def set_intel(game, intel):
    st.session_state.active_game = game
    st.session_state.active_intel = intel

# --- 4. THE BOARD ---
st.title("🏛️ EDGEINTEL SYNDICATE")
st.markdown("""<div class="whale-card">
    <div style="color: #00F5D4; font-weight: 800; font-size: 0.75rem
