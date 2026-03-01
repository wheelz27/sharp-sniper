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
    "NBA: Spurs @ Knicks": {"status": "FINAL", "edge": "NYK -12.5", "conf": "WIN", "intel": "Knicks dominated the paint. Final: 114-89."},
    "NBA: Wolves @ Nuggets": {"status": "LIVE (Q2)", "edge": "DEN -3.5", "conf": "88%", "intel": "Nuggets trailing 50-58. Jokic 12 reb. Model expects 2H interior surge."},
    "NBA: Bucks @ Bulls": {"status": "LIVE (Q3)", "edge": "MIL -11.5", "conf": "91%", "intel": "Bucks lead 71-59. Giannis 22 pts. Mismatch in transition D holding firm."},
    "NBA: Cavs @ Nets": {"status": "LIVE (Q2)", "edge": "CLE -4.5", "conf": "82%", "intel": "Nets lead 52-46. Cavs shooting 22% from deep; model expects mean reversion."},
    "NBA: 76ers @ Celtics": {"status": "8:00 PM ET", "edge": "BOS -9.5", "conf": "94%", "intel": "Embiid/George OUT. Celtics net rating +14.2 at home. Pick: CELTICS -9.5."},
    "NBA: Kings @ Lakers": {"status": "9:30 PM ET", "edge": "LAL -13.0", "conf": "85%", "intel": "Lakers transition speed mismatch vs Kings tired rotation. Pick: LAKERS -13.0."},
    
    "NHL: Knights @ Penguins": {"status": "FINAL", "edge": "PIT ML", "conf": "WIN", "intel": "Penguins shutout Knights 2-0. Silovs 22 saves."},
    "NHL: Jets @ Sharks": {"status": "LIVE (P2)", "edge": "WPG ML", "conf": "89%", "intel": "Jets lead 1-0. Sharks struggling with zone entries."},
    "NHL: Panthers @ Islanders": {"status": "6:30 PM ET", "edge": "FLA ML", "conf": "86%", "intel": "Florida 1st game since break. Islanders PK unit bottom-10. Pick: FLA ML."},
    
    "NCAAB: Michigan St @ Indiana": {"status": "LIVE (H2)", "edge": "MSU -2.5", "conf": "91%", "intel": "Sparty lead 45-37. Interior defense neutralizing Indiana's post usage."},
    
    "MLS: Orlando vs Inter Miami": {"status": "7:00 PM ET", "edge": "MIA ML", "conf": "83%", "intel": "Messi/Suarez starting. Orlando missing key CB. Pick: MIAMI ML."},
    
    "TENNIS: WTA Austin Final": {"status": "FINAL", "edge": "STEARNS ML", "conf": "WIN", "intel": "Stearns def. Townsend 7-6, 7-5. Home court energy was the deciding factor."},
    "TENNIS: Mérida Open Final": {"status": "7:00 PM ET", "edge": "OVER 21.5", "conf": "79%", "intel": "Humidity slows court speed; expects a 3-set struggle between Bucsa and Frech."},
    "TENNIS: Indian Wells Qualies": {"
