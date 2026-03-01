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
        {"game": "Knicks @ Spurs", "spread": "SAS -1.5", "prop": "Wemby O 4.5 BLK", "intel": "Potential Finals preview. Both healthy. Knicks won last 2 matchups, but Spurs at home are 43-16."},
        {"game": "76ers @ Celtics", "spread": "BOS -9.5", "prop": "J. Brown O 29.5 PTS", "intel": "Embiid (Oblique) OUT. Tatum (Achilles) OUT. Brown usage spikes 12% as the solo engine."},
        {"game": "Kings @ Lakers", "spread": "LAL -13.0", "prop": "Luka O 11.5 AST", "intel": "Luka/LeBron active. Kings tanking (14-47). Lakers' transition efficiency is elite tonight."}
    ],
    "NHL": [
        {"game": "Panthers @ Islanders", "spread": "FLA -145", "prop": "Barkov 1+ Point", "intel": "NYI 1-7 immediately after Olympic breaks. Florida 100% healthy; massive xG edge."},
        {"game": "Flames @ Ducks", "spread": "ANA -1.5", "prop": "McTavish O 0.5 PTS", "intel": "Ducks won 4 straight. Calgary on back-to-back road leg. McTavish 72% hit rate at home."},
        {"game": "Blackhawks @ Mammoth", "spread": "UTA -310", "prop": "L. Cooley Goal", "intel": "Utah Mammoth (69% win prob). Cooley returned from injury with goals in 2 straight games."}
    ],
    "TENNIS": [
        {"game": "MGM Slam: Kyrgios/Bublik", "
