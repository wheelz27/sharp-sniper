import streamlit as st
import pandas as pd
from engine.matchups import MatchupAnalyzer
import config

# --- 1. PREMIUM UI STYLING ---
st.set_page_config(page_title="EDGEINTEL | SYNDICATE", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .funnel-box { 
        background: linear-gradient(135deg, #1f6feb 0%, #0d1117 100%);
        padding: 30px; border-radius: 12px; border: 1px solid #388bfd; text-align: center;
        margin-bottom: 30px;
    }
    .join-btn {
        background-color: #238636; color: white !important; padding: 12px 24px;
        text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;
    }
    .matrix-header { color: #58a6ff; font-family: monospace; letter-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE SALES FUNNEL ---
st.markdown("""
    <div class="funnel-box">
        <h1 style='margin-bottom:0;'>🎯 UNLOCK THE SNIPER SYNDICATE</h1>
        <p style='font-size: 1.2rem; opacity: 0.8;'>Get automated +264 Parlay Alerts sent to your phone via Private Discord.</p>
        <br>
        <a href="https://whop.com/YOUR_LINK" class="join-btn">JOIN NOW — SECURE YOUR EDGE</a>
    </div>
""", unsafe_allow_html=True)

# --- 3. LIVE INTELLIGENCE FEED (THE PROOF) ---
st.markdown("<h3 class='matrix-header'>📡 LIVE MARKET INTELLIGENCE</h3>", unsafe_allow_html=True)

try:
    with st.spinner("Analyzing Market Inefficiencies..."):
        # We use NBA or NCAAB based on the sidebar
        sport = st.sidebar.radio("Active Theater", ["NBA", "NCAAB"])
        analyzer = MatchupAnalyzer(sport=sport.lower())
        all_edges = analyzer.compute_all_edges()

        if all_edges:
            # We show the public some analysis to prove the model works
            df = pd.DataFrame([{
                "MATCHUP": f"{e.away_team} @ {e.home_team}",
                "VEGAS": f"{e.market_spread_home:+.1f}",
                "EDGEINTEL MODEL": f"{e.model_spread_home:+.1f}",
                "DIFFERENTIAL": f"{e.spread_edge:+.1f} PTS",
                "CONFIDENCE": f"{e.confidence}%"
            } for e in all_edges[:5]]) # Show first 5 games as the "Free Sample"
            
            st.table(df)
            st.info("Showing 5 of 15 analyzed games. Full board available in the Private Discord.")
        else:
            st.warning("⚠️ Market is currently tight. Refreshing for new edges...")

except Exception as e:
    st.error(f"Engine is warming up. Please refresh. Error: {e}")
