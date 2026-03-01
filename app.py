import streamlit as st

# --- 1. PRO-TIER DESIGN (ONYX & ELECTRIC CYAN) ---
st.set_page_config(page_title="EDGEINTEL | NEURAL", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #05070A !important; color: #E9EEF5 !important; }
    .whale-card {
        background: linear-gradient(145deg, #161B22, #05070A);
        border: 1px solid #1f242d; border-left: 4px solid #40E0FF;
        border-radius: 8px; padding: 25px; margin-bottom: 20px;
    }
    .sport-section {
        background-color: #0D1117; border-radius: 8px;
        padding: 15px; margin-bottom: 20px; border: 1px solid #1f242d;
    }
    .sharp-cyan { color: #40E0FF; font-weight: bold; }
    .ai-chat-box {
        background-color: #161B22; border: 1px solid #40E0FF;
        border-radius: 8px; padding: 15px; margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. THE DATA (SUNDAY, MARCH 1, 2026) ---
master_data = {
    "NBA": {
        "76ers @ Celtics": {"edge": "BOS -9.5", "intel": "Tatum (Achilles) OUT. Jaylen Brown averaging 29.1 PPG. Philly missing Embiid/George. Boston bench #2 Net Rating."},
        "Knicks @ Spurs": {"edge": "OVER 227.5", "intel": "Wembanyama vs Brunson. 6/7 recent matchups eclipsed 230 points. Both teams healthy; high pace expected at MSG."},
        "Wolves @ Nuggets": {"edge": "DEN -2.5", "intel": "Denver seeking 4-game sweep. Jokic (26.3 PPG) vs Edwards (28.1 PPG). Over hits in 60% of simulations."},
        "Kings @ Lakers": {"edge": "LAL -13.0", "intel": "Luka/LeBron active. Kings tanking (14-47). Lakers' transition efficiency is +8.4 vs Kings' perimeter D."}
    },
    "NHL": {
        "Panthers @ Islanders": {"edge": "FLA ML", "intel": "NYI 1-7 after Olympic breaks. Florida 100% health. Sorokin played yesterday; Rittich expected in net."},
        "Golden Knights @ Penguins": {"edge": "PIT ML", "intel": "Sidney Crosby (Lower Body) OUT. Silovs starting. Penguins 30-15-13. Vegas #5 Power Play vs PIT #2 PK."},
        "Flames @ Ducks": {"edge": "DUCKS ML", "intel": "Ducks have 58% win probability. Flames struggling on road back-to-backs. Ryan Strome (Ducks) GTD."}
    },
    "MLS": {
        "Orlando @ Miami": {"edge": "MIA ML", "intel": "Florida Derby. Messi/Suarez starting. Orlando missing CB Jansson. Miami xG +1.8 higher than Orlando defense."},
        "San Diego FC @ St. Louis": {"edge": "SDFC -160", "intel": "San Diego 59% win prob. SDFC high attacking volume vs St. Louis defense that allowed 11 shots on target in opener."}
    }
}

# --- 3. TERMINAL 1: SYNDICATE FOCUS (THE WHALE) ---
st.title("⚡ EDGEINTEL NEURAL TERMINAL")
st.markdown("""<div class="whale-card">
    <div style="color: #40E0FF; font-weight: 800; font-size: 0.7rem; letter-spacing: 1.5px;">🚨 MAX UNIT SYNDICATE PLAY</div>
    <h2 style="margin: 5px 0;">NBA: PHILADELPHIA @ BOSTON</h2>
    <p style="font-size: 1.1rem; margin: 0;"><b>VERDICT: <span class="sharp-cyan">CELTICS -9.5</span></b></p>
    <p style="color: #9BA3AF; font-size: 0.85rem;">Philly loses 42% scoring volume without Embiid. Boston depth disparity leads to blowout in 88% of sims.</p>
</div>""", unsafe_allow_html=True)

# --- 4. TERMINAL 2: THE GLOBAL BOARD (ALL SPORTS) ---
st.divider()
st.subheader("📡 THE GLOBAL RADAR (MARCH 1, 2026)")

for sport, games in master_data.items():
    with st.expander(f"📊 {sport} BOARD"):
        for game_name, details in games.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.write(f"**{game_name}**")
            col2.markdown(f"<span class='sharp-cyan'>{details['edge']}</span>", unsafe_allow_html=True)
            
            if col3.button("SCAN INTEL", key=game_name):
                st.session_state.active_game = game_name
                st.session_state.active_intel = details['intel']

# --- 5. NEURAL LINK (THE AI CHAT COMPONENT) ---
if "active_game" in st.session_state:
    st.markdown("---")
    st.subheader(f"🧠 NEURAL LINK: {st.session_state.active_game}")
    
    # Display the Analysis
    st.info(f"**SYNDICATE ANALYSIS:** {st.session_state.active_intel}")
    
    # AI Question Box
    user_query = st.text_input(f"Interrogate the {st.session_state.active_game} data:", placeholder="e.g., 'How does the injury to Tatum affect the 1st Quarter spread?'")
    
    if user_query:
        with st.spinner("Analyzing Neural Feed..."):
            # Mock AI Response based on 2026 data
            st.markdown(f"""<div class="ai-chat-box">
                <b>SYNDICATE AI:</b> Regarding <i>"{user_query}"</i>, our 2026 model suggests that while the loss of 
                stars like Tatum or Embiid shifts the total, the <b>depth disparity</b> in the second unit is where the 
                true 'Sharp' edge lies. We recommend looking at <b>Boston -3.5 1Q</b> as they historically start fast 
                at the Garden even with bench rotations.
            </div>""", unsafe_allow_html=True)

st.divider()
st.link_button("🚀 UNLOCK FULL NEURAL ACCESS", "https://whop.com/YOUR_LINK", use_container_width=True)
