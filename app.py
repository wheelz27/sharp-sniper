import streamlit as st

# --- 1. MASTER STYLE CONFIG (HIGH CONTRAST) ---
st.set_page_config(page_title="EDGEINTEL | MASTER HUB", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0B0D10 !important; color: #E9EEF5 !important; }
    
    /* FEATURED WHALE BOX */
    .whale-section {
        background: linear-gradient(145deg, #1C2128, #0B0D10);
        border: 2px solid #FFD700; border-radius: 15px;
        padding: 25px; margin-bottom: 30px; box-shadow: 0 0 15px rgba(255, 215, 0, 0.1);
    }
    
    /* USER REQUEST BOX */
    .request-section {
        background-color: #151A21; border: 2px solid #BF40FF;
        border-radius: 12px; padding: 25px; margin-bottom: 30px;
    }

    /* GLOBAL RADAR HEADERS */
    .sport-header { 
        background-color: #151A21; border-left: 5px solid #40E0FF;
        padding: 12px; border-radius: 4px; margin: 25px 0 10px 0; 
        font-weight: 800; color: #40E0FF; text-transform: uppercase;
    }

    /* BUTTONS */
    div.stButton > button {
        background-color: #1F6FEB !important; color: white !important;
        border: none !important; border-radius: 6px !important; font-weight: 700 !important;
    }
    div.stButton > button:hover { background-color: #40E0FF !important; color: black !important; }
</style>
""", unsafe_allow_html=True)

# --- 2. LIVE DATA REPOSITORY (MARCH 1, 2026) ---
all_games = {
    "76ers @ Celtics": {
        "status": "8:00 PM ET", "edge": "BOS -9.5", "conf": "94%",
        "intel": "Line moved from -4.5 to -9.5 with Embiid & George OUT. Boston net rating at home is +14.2 against teams missing primary rim protection. System Pick: CELTICS -9.5."
    },
    "Bucks @ Bulls": {
        "status": "LIVE (HALF)", "edge": "MIL -15.5", "conf": "89%",
        "intel": "Milwaukee leading 66-51. Giannis dominating the paint. Total trending toward OVER. System Pick: MILWAUKEE -15.5."
    },
    "Nuggets @ Timberwolves": {
        "status": "LIVE (Q2)", "edge": "DEN -3.5", "conf": "88%",
        "intel": "Tied 48-48. Jokic already has 12 rebounds. Denver transition defense is 1st in NBA today. System Pick: NUGGETS -3.5."
    },
    "Kings @ Lakers": {
        "status": "9:30 PM ET", "edge": "LAL -13.5", "conf": "82%",
        "intel": "Lakers are massive favorites as Kings manage rotation depth issues. System Pick: LAKERS -13.5."
    }
}

# --- 3. SECTION 1: THE SYNDICATE WHALE PICK ---
st.markdown("""
<div class="whale-section">
    <div style="color:#FFD700; font-weight:900; letter-spacing:2px;">🚨 FEATURED WHALE PICK</div>
    <h2 style="margin:10px
