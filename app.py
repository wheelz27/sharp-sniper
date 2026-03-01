import streamlit as st

# --- 1. 2026 CLUBROOM CONTRAST THEME ---
st.set_page_config(page_title="EDGEINTEL | PRO", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0A0C10 !important; color: #E9EEF5 !important; }
    
    /* Syndicate Whale Card */
    .whale-card {
        background: linear-gradient(145deg, #161B22, #0A0C10);
        border: 1px solid #1f242d;
        border-left: 4px solid #40E0FF;
        border-radius: 8px; padding: 25px; margin-bottom: 35px;
    }

    /* Sport Headers */
    .sport-header {
        background-color: #161B22;
        border-left: 3px solid #40E0FF;
        padding: 8px 15px; margin: 25px 0 10px 0;
        font-weight: 700; color: #40E0FF;
        text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1.5px;
    }

    .sharp-blue { color: #40E0FF; font-weight: 700; }
    .muted-intel { color: #9BA3AF; font-size: 0.9rem; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# --- 2. ACTUAL SYNDICATE DATA (SUNDAY, MARCH 1, 2026) ---
master_data = {
    "NBA: Kings @ Lakers": {"status": "9:30 PM ET", "edge": "LAL -13.0", "intel": "Luka Doncic (32.6 PPG) leads the NBA. Lakers are +4 in scoring differential. Kings missing Zach LaVine (Season Out) and Sabonis. This is a mismatch in transition volume."},
    "NBA: Bucks @ Bulls": {"status": "LIVE", "edge": "CHI +6.5", "intel": "Giannis Antetokounmpo (Calf) is officially OUT. Milwaukee's offensive rating drops by 11.4 points without him. Value is on the home dog."},
    "NHL: Panthers @ Islanders": {"status": "6:30 PM ET", "edge": "FLA ML", "intel": "First game for NYI after Olympic break. History shows home teams are 1-7 in this spot. Panthers have Kulikov back and are top-5 in xG."},
    "MLS: Orlando @ Miami": {"status": "7:00 PM ET", "edge": "MIA ML", "intel": "The Florida Derby. Messi and Suarez are starting. Orlando missing key defender Robin Jansson. Miami xG is +1.8 higher than the Lions' current setup."},
    "TENNIS: Indian Wells": {"status": "LIVE", "edge": "UNDER", "intel": "Qualifying Day 1. Early sensor data shows court speed is 4% slower than 2025. Favors defensive grinders. Rakhimova and Timofeeva already secured 2-set wins."}
}

# --- 3. THE WHALE (MAX UNIT PLAY) ---
st.markdown("""
<div class="whale-card">
    <div style="color: #40E0FF; font-weight: 800; font-size: 0.7rem; letter-spacing: 1.5px; margin-bottom:10px;">🚨 MAX UNIT SYNDICATE PLAY</div>
    <h2 style="margin: 0;">SACRAMENTO KINGS @ LA LAKERS</h2>
    <p style="font-size: 1.2rem; margin: 5px 0;"><b>VERDICT: <span class="sharp-blue">LAKERS -13.0</span></b></p>
    <p class="muted-intel">
        <b>SHARP LOGIC:</b> Sacramento has 5 players on the injury report, including LaVine. 
        Luka Doncic is shooting 35.4% from deep and the Lakers' transition engine is currently #1 in the West. Expect
