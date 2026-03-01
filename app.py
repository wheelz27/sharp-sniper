import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. PREMIUM HUD STYLING ---
st.set_page_config(page_title="EDGEINTEL | SYNDICATE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #06090f; color: #e6edf3; }
    .command-header {
        background: rgba(23, 27, 33, 0.8);
        border: 1px solid #30363d; border-left: 5px solid #238636;
        padding: 25px; border-radius: 12px; margin-bottom: 20px;
    }
    .pulse {
        display: inline-block; width: 10px; height: 10px;
        border-radius: 50%; background: #238636;
        animation: pulse-green 2s infinite; margin-right: 10px;
    }
    @keyframes pulse-green {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(35, 134, 54, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(35, 134, 54, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(35, 134, 54, 0); }
    }
    .stTable { background-color: #161b22; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. COMMAND HEADER ---
st.markdown(f"""
    <div class="command-header">
        <h1 style='margin:0; font-family: monospace;'>📡 <span class="pulse"></span>EDGEINTEL COMMAND CENTER</h1>
        <p style='color: #8b949e;'>NEURAL ENGINE v3.4 | LAST SYNC: {datetime.now().strftime('%H:%M:%S')}</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. LIVE INTELLIGENCE MATRIX (THE INSIGHT) ---
st.subheader("📊 Live Market Projection Matrix")
st.write("Comparing Neural Model Fair-Value to Vegas Spreads")

# We use the Analyzer but ensure it returns DATA even if the edge is small
try:
    from engine.matchups import MatchupAnalyzer
    sport = st.sidebar.radio("Active Theater", ["NBA", "NCAAB"])
    analyzer = MatchupAnalyzer(sport=sport.lower())
    all_games = analyzer.compute_all_edges()

    if all_games:
        # This table shows the "Why" by comparing Vegas to Your Model
        df = pd.DataFrame([{
            "GAME": f"🏀 {e.away_team} @ {e.home_team}",
            "VEGAS": f"{e.market_spread_home:+.1f}",
            "OUR MODEL": f"{e.model_spread_home:+.1f}",
            "THE EDGE": f"🔥 {e.spread_edge:+.1f} PTS",
            "PROBABILITY": f"{e.confidence}%"
        } for e in all_games])
        st.table(df)
    else:
        # Fallback to show the user the dashboard structure while lines load
        st.info("🔄 Scanning Market... Projections populating as Vegas releases rotations.")
except Exception as e:
    st.error(f"Engine Standby: {e}")

# --- 4. THE SYNDICATE PAYWALL (THE FUNNEL) ---
st.divider()
col_a, col_b = st.columns([1.5, 1])

with col_a:
    st.markdown("""
        <div style="background: rgba(35, 134, 54, 0.1); border: 1px solid #238636; padding: 25px; border-radius: 12px;">
            <h3 style="color:#3fb950; margin-top:0;">🔓 ACTIVE SNIPER PARLAY (+264)</h3>
            <p style="color:#8b949e; font-family: monospace;">[LEG 1] LAL +5.5 (LOCKED)</p>
            <p style="color:#8b949e; font-family: monospace;">[LEG 2] PHI -1.5 (LOCKED)</p>
            <p style="color:#8b949e; font-family: monospace;">[LEG 3] OVER 224.5 (LOCKED)</p>
        </div>
    """, unsafe_allow_html=True)

with col_b:
    st.write("### Secure Your Edge")
    st.write("Stop betting on luck. Join the elite syndicate and get automated sniper alerts sent to your phone.")
    st.link_button("🚀 JOIN THE SYNDICATE ON WHOP", "
