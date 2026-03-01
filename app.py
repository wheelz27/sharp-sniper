import streamlit as st
import pandas as pd
from engine.matchups import MatchupAnalyzer # Connects to your real logic

# --- 1. PREMIUM UI (STAYING IMPRESSIVE) ---
st.set_page_config(page_title="EDGEINTEL | SYNDICATE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .command-header {
        background: rgba(23, 27, 33, 0.8);
        border: 1px solid #30363d; border-left: 5px solid #238636;
        padding: 30px; border-radius: 12px; margin-bottom: 25px;
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
    </style>
""", unsafe_allow_html=True)

# --- 2. THE COMMAND HEADER ---
st.markdown("""
    <div class="command-header">
        <h1 style='margin:0; font-family: monospace;'>📡 <span class="pulse"></span>EDGEINTEL COMMAND CENTER</h1>
        <p style='color: #8b949e; letter-spacing: 1px;'>REAL-TIME MARKET ARBITRAGE ACTIVE</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. THE LIVE ENGINE CALL ---
try:
    sport = st.sidebar.radio("Theater", ["NBA", "NCAAB"])
    analyzer = MatchupAnalyzer(sport=sport.lower())
    real_games = analyzer.compute_all_edges() # PULLING REAL DATA

    if real_games:
        st.subheader("📊 Live Market Projection Matrix")
        
        # Mapping real engine data to the pretty UI
        df = pd.DataFrame([{
            "GAME": f"🏀 {e.away_team} @ {e.home_team}",
            "VEGAS": f"{e.market_spread_home:+.1f}",
            "MODEL": f"{e.model_spread_home:+.1f}",
            "EDGE": f"🔥 {e.spread_edge:+.1f}",
            "PROB": f"{e.confidence}%"
        } for e in real_games])

        st.table(df)
    else:
        st.info("Searching for market inefficiencies... No active 2.0+ edges found currently.")

except Exception as e:
    st.error("Connecting to Neural Engine... Please refresh in 30 seconds.")

# --- 4. THE PAYWALL ---
st.divider()
st.link_button("🚀 JOIN THE SYNDICATE TO UNLOCK SNIPER PARLAYS", "https://whop.com/YOUR_LINK", use_container_width=True)
