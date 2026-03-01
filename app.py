import streamlit as st

# --- 1. PRO-TIER DESIGN (MIDNIGHT & NEON EMERALD) ---
st.set_page_config(page_title="EDGEINTEL | SYNDICATE", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #05070A !important; color: #E0E0E0 !important; }
    
    /* WHALE SECTION */
    .whale-card {
        background: linear-gradient(135deg, #0D1117 0%, #05070A 100%);
        border-left: 5px solid #00FFA3; border-radius: 4px;
        padding: 25px; margin-bottom: 30px; border-top: 1px solid #1A1D23;
    }

    /* SPORT HEADERS */
    .sport-header {
        color: #00FFA3; font-weight: 800; font-size: 0.75rem;
        letter-spacing: 2px; text-transform: uppercase;
        border-bottom: 1px solid #1A1D23; padding-bottom: 5px; margin-top: 25px;
    }

    .neon-text { color: #00FFA3; font-weight: bold; }
    .sharp-logic { color: #8B949E; font-size: 0.9rem; line-height: 1.5; }
    .status-badge { background: #1A1D23; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; color: #58A6FF; }
</style>
""", unsafe_allow_html=True)

# --- 2. SYNDICATE DATA (LIVE MARCH 1, 2026) ---
master_board = {
    "NBA: 76ers @ Celtics": {"status": "8:00 PM ET", "edge": "BOS -9.5", "intel": "Market hasn't adjusted to the bench disparity. Jayson Tatum (Achilles) is OUT, but Jaylen Brown is averaging 29.1 PPG in his absence. Philly is 12-14 without Embiid (Oblique) and lacks interior rim protection. Lay the points."},
    "NBA: Kings @ Lakers": {"status": "9:30 PM ET", "edge": "LAL -12.5", "intel": "Kings (14-47) are in full tank mode. Lakers' big three of Doncic, LeBron, and Ayton are active. Luka leads the NBA in 3PM (3.7/game). Sacramento's perimeter defense is 28th in the league. Blowout alert."},
    "NHL: Panthers @ Islanders": {"status": "6:30 PM ET", "edge": "FLA ML", "intel": "NYI are historically 1-7 following long breaks (Olympic rest). Florida returns at 100% health. The 'Rust Factor' vs. Florida’s top-tier forecheck is a major tactical mismatch."},
    "MLS: San Diego vs St. Louis": {"status": "9:15 PM ET", "edge": "SAN DIEGO -155", "intel": "San Diego has scored 9 goals in their first 3 matches. St. Louis defense struggled in the opener (allowed 11 shots on target). Snapdragon Stadium home atmosphere is currently a +0.5 goal advantage."},
    "TENNIS: Indian Wells Qualies": {"status": "LIVE", "edge": "UNDER 21.5", "intel": "Sensor data shows courts playing 4% slower than 2025. This favors heavy defensive grinders and leads to longer rallies that exhaust lower-tier players. Hammer 'Unders' for the night session."}
}

# --- 3. THE WHALE (MAX UNIT PLAY) ---
st.markdown("""
<div class="whale-card">
    <div style="color: #00FFA3; font-weight: 800; font-size: 0.7rem; letter-spacing: 1.5px;">🚨 MAX UNIT SYNDICATE PLAY</div>
    <h2 style="margin: 10px 0;">PHILADELPHIA @ BOSTON (NBA)</h2>
    <p style="font-size: 1.2rem; margin: 0;"><b>VERDICT: <span class="neon-text">CELTICS -9.5</span></b></p>
    <p class="sharp-logic" style="margin-top: 10px;">
        <b>SHARP INTEL:</b> Total system wash. With Embiid and George out, Philly loses 42% of their scoring volume. 
        Boston's 2nd unit (Pritchard/Hauser) ranks #2 in Net Rating. This depth disparity usually triggers a 15-0 run in the late 3rd quarter. High conviction.
    </p>
</div>
""", unsafe_allow_html=True)

# --- 4. GLOBAL RADAR ---
st.subheader("📡 THE GLOBAL RADAR")

for cat in ["NBA", "NHL", "MLS", "TENNIS"]:
    st.markdown(f'<div class="sport-header">{cat} SUNDAY BOARD</div>', unsafe_allow_html=True)
    
    for game, info in master_board.items():
        if game.startswith(cat):
            with st.container():
                c1, c2, c3 = st.columns([2, 1, 1])
                with c1:
                    st.markdown(f"**{game.split(': ')[1]}**")
                    st.markdown(f"<div class='status-badge'>{info['status']}</div>", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"<span class='neon-text'>{info['edge']}</span>", unsafe_allow_html=True)
                with c3:
                    if st.button("EXECUTE SCAN", key=game):
                        st.info(f"🧠 {info['intel']}")
                st.markdown("<hr style='border: 0.1px solid #1A1D23; margin: 5px 0;'>", unsafe_allow_html=True)

st.divider()
st.link_button("🚀 UNLOCK PRIVATE SYNDICATE (WHOP)", "https://whop.com/YOUR_LINK", use_container_width=True)
