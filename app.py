import streamlit as st

# --- 1. PRO-TIER DESIGN (MIDNIGHT NAVY & ELECTRIC CYAN) ---
st.set_page_config(page_title="EDGEINTEL | SYNDICATE", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0A0C10 !important; color: #E9EEF5 !important; }
    
    /* SYNDICATE WHALE CARD - CLUBROOM CONTRAST */
    .whale-card {
        background: linear-gradient(145deg, #161B22, #0A0C10);
        border: 1px solid #1f242d;
        border-left: 4px solid #40E0FF;
        border-radius: 8px; padding: 25px; margin-bottom: 35px;
    }

    /* SPORT HEADERS */
    .sport-header {
        background-color: #161B22; border-left: 3px solid #40E0FF;
        padding: 8px 15px; margin: 25px 0 10px 0;
        font-weight: 700; color: #40E0FF;
        text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1.5px;
    }

    .sharp-cyan { color: #40E0FF; font-weight: bold; }
    .intel-text { color: #9BA3AF; font-size: 0.95rem; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# --- 2. THE SYNDICATE BOARD (LIVE SUNDAY, MARCH 1, 2026) ---
master_data = {
    "NBA: 76ers @ Celtics": {"status": "8:00 PM ET", "edge": "BOS -9.5", "intel": "Jayson Tatum (Achilles) is officially OUT. However, Jaylen Brown is averaging 29.1 PPG in his absence. Philly is gutted: No Embiid or George. The Celtics home net rating is +14.2 against shorthanded rivals. Lay the points."},
    "NBA: Bucks @ Bulls": {"status": "LIVE", "edge": "CHI +6.5", "intel": "Giannis (Calf) is OUT. Milwaukee's offensive rating drops by 11.4 points without him. Chicago is on a 2-13 ATS skid, but the line movement toward the Bulls suggests sharp money is fading the shorthanded Bucks."},
    "NBA: Kings @ Lakers": {"status": "9:30 PM ET", "edge": "LAL -12.5", "intel": "Lakers' Luka/LeBron/Ayton trio is active. Luka leads the NBA in 3PM. Sacramento is in full tank mode, missing Sabonis and LaVine. Target the Lakers transition overs."},
    "NHL: Panthers @ Islanders": {"status": "6:30 PM ET", "edge": "FLA ML", "intel": "NYI are 1-7 in home openers following long breaks (Olympic rest). Florida is 100% healthy. Huge edge in expected goals (xG) for the Cats tonight."},
    "MLS: Orlando @ Miami": {"status": "7:00 PM ET", "edge": "MIA ML", "intel": "Florida Derby. Messi and Suarez are starting. Miami seeking their first goal of 2026 after the LAFC shutout. Orlando missing key CB Jansson."},
    "TENNIS: Austin Final": {"status": "FINAL", "edge": "STEARNS ML", "intel": "WIN. Peyton Stearns def. Taylor Townsend 7-6, 7-5. The UT Alum used the home-court energy to secure her second WTA title."},
    "TENNIS: Indian Wells Qualies": {"status": "LIVE", "edge": "UNDER 21.5", "intel": "Sensor data shows courts playing 4% slower than 2025. This favors defensive grinders. Look for 'Unders' in matches involving heavy baseline ralliers."}
}

# --- 3. THE WHALE (MAX UNIT PLAY) ---
st.markdown("""
<div class="whale-card">
    <div style="color: #40E0FF; font-weight: 800; font-size: 0.7rem; letter-spacing: 1.5
