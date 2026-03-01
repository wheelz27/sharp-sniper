import streamlit as st

# --- 1. THEME CONFIG ---
st.set_page_config(page_title="EDGEINTEL | FULL BOARD", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0B0D10 !important; color: #E9EEF5 !important; }
    .whale-section { background: linear-gradient(145deg, #1C2128, #0B0D10); border: 2px solid #FFD700; border-radius: 15px; padding: 25px; margin-bottom: 30px; }
    .request-section { background-color: #151A21; border: 2px solid #BF40FF; border-radius: 12px; padding: 25px; margin-bottom: 30px; }
    .sport-header { background-color: #151A21; border-left: 5px solid #40E0FF; padding: 10px 15px; margin: 25px 0 10px 0; font-weight: 800; color: #40E0FF; text-transform: uppercase; font-size: 0.85rem; }
    .game-row { border-bottom: 1px solid #30363d; padding: 10px 0; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE TOTAL SUNDAY BOARD (MARCH 1, 2026) ---
master_data = {
    # NBA SLATE
    "NBA: Spurs @ Knicks": {"status": "FINAL", "edge": "NYK -12.5", "conf": "WIN", "intel": "Knicks dominated the paint as predicted. FINAL: 114-89."},
    "NBA: Timberwolves @ Nuggets": {"status": "LIVE (Q2)", "edge": "DEN -3.5", "conf": "88%", "intel": "Nuggets trailing 50-58. Jokic 12 reb. System predicts 2H surge."},
    "NBA: Bucks @ Bulls": {"status": "LIVE (Q3)", "edge": "MIL -11.5", "conf": "91%", "intel": "Bucks lead 71-59. Giannis 22 pts. Interior mismatch holding firm."},
    "NBA: Cavaliers @ Nets": {"status": "LIVE (Q2)", "edge": "CLE -4.5", "conf": "82%", "intel": "Nets lead 52-46. Cavs shooting cold from deep; model expects mean reversion."},
    "NBA: 76ers @ Celtics": {"status": "8:00 PM ET", "edge": "BOS -9.5", "conf": "94%", "intel": "Embiid/George OUT. Boston is 39-22. System Pick: CELTICS -9.5."},
    "NBA: Kings @ Lakers": {"status": "9:30 PM ET", "edge": "LAL -13.0", "conf": "85%", "intel": "Kings depth issues vs Lakers transition speed. System Pick: LAKERS -13.0."},
    "NBA: Grizzlies @ Pacers": {"status": "5:00 PM ET", "edge": "IND -2.5", "conf": "80%", "intel": "Pacers home court rest advantage. Pick: PACERS -2.5."},

    # NHL SLATE
    "NHL: Knights @ Penguins": {"status": "FINAL", "edge": "PIT ML", "conf": "WIN", "intel": "Penguins shutout Knights 2-0. Silovs 22 saves."},
    "NHL: Blackhawks @ Utah Mammoth": {"status": "LIVE (P2)", "edge": "UTAH -1.5", "conf": "84%", "intel": "Mammoth trailing 0-1. Expect power play adjustment in P3."},
    "NHL: Jets @ Sharks": {"status": "LIVE (P2)", "edge": "WPG ML", "conf": "89%", "intel": "Jets lead 1-0. Sharks struggling with zone entries."},
    "NHL: Panthers @ Islanders": {"status": "6:30 PM ET", "edge": "FLA ML", "conf": "86%", "intel": "Islanders first home game since Olympic break. Pick: PANTHERS ML."},

    # NCAAB SLATE
    "NCAAB: Michigan St @ Indiana": {"status": "3:45 PM ET", "edge": "MSU -2.5", "conf": "91%", "intel": "Sparty's defense vs Indiana's post-heavy usage. Pick: MSU -2.5."},
    "NCAAB: Purdue @ Ohio St": {"status": "LIVE (H1)", "edge": "PUR -5.5", "conf": "87%", "intel": "Ohio St leading 36-31. Edey early foul trouble. System anticipates 2H bounce."},

    # MLS SLATE
    "MLS: Philadelphia @ NYCFC": {"status": "LIVE", "edge": "DRAW", "conf": "75%", "intel": "0-0 Defensive struggle at Subaru Park."},
    "MLS: Orlando vs Inter Miami": {"status": "7:00 PM ET", "edge": "MIA ML", "conf": "83%", "intel": "Messi/Suarez starting. Orlando missing key CB. Pick: MIAMI ML."},
    "MLS: Austin FC vs D.C. United": {"status": "9:30 PM ET", "edge": "ATX ML", "conf": "79%", "intel": "Austin 3-0 all-time vs DC. Home atmosphere at Q2 is elite. Pick: AUSTIN FC."},

    # TENNIS SLATE
    "TENNIS: WTA Austin Final": {"status": "LIVE", "edge": "STEARNS ML", "conf": "84%", "intel": "Stearns vs Townsend. Flat groundstrokes favor Stearns in these conditions."},
    "TENNIS: Indian Wells Qualies": {"status": "LIVE", "edge": "GRINDERS", "conf": "88%", "intel": "Court speed is 4
