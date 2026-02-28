import streamlit as st
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

# Import your existing engine components
from engine.matchups import MatchupAnalyzer
from engine.edge import rank_edges
from engine.tracking import PickTracker
import config

# --- 1. SETTINGS & THEME ---
st.set_page_config(page_title="EDGEINTEL | COMMAND CENTER", layout="wide", page_icon="🎯")

# Terminal-style Dark Mode CSS
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .parlay-card { 
        background: linear-gradient(135deg, #238636 0%, #0d1117 100%);
        border: 1px solid #2ea043; padding: 25px; border-radius: 12px; margin-bottom: 25px;
    }
    .strategy-box { background-color: #161b22; border-left: 4px solid #388bfd; padding: 20px; border-radius: 0 8px 8px 0; }
    </style>
""", unsafe_allow_html=True)

# --- 2. DATA PIPELINE ---
@st.cache_data(ttl=600)
def run_intelligence_engine(sport_choice):
    """Triggers your existing MatchupAnalyzer pipeline"""
    # Initialize the analyzer from engine/matchups.py
    analyzer = MatchupAnalyzer(sport=sport_choice.lower())
    
    # HANDSHAKE FIX: Changed from .run() to .compute_all_edges() to match your engine
    edges = analyzer.compute_all_edges() 
    return edges, analyzer

# --- 3. HEADER & STRATEGY EXPLAINER ---
st.title("🎯 EdgeIntel Intelligence Hub")

with st.expander("📖 SYSTEM ARCHITECTURE: THE 90% CLV STRATEGY"):
    st.markdown("""
    <div class="strategy-box">
    <h3>The Mathematical Edge</h3>
    <p>This engine is designed to exploit <b>Market Lags</b> before the closing bell.</p>
    <ul>
        <li><b>Form vs. Season:</b> We weigh the full season at 55% but aggressively track the 'Last 5 Games' at 15% to catch regime shifts.</li>
        <li><b>The CLV Pillar:</b> Consistently beating the closing line is the only way to professional profit.</li>
        <li><b>Sniper Logic:</b> We only show plays where the model-to-market disagreement exceeds 2.0 points.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR OPERATIONS ---
with st.sidebar:
    st.header("🕹️ CONTROL PANEL")
    sport = st.radio("Active Theater", ["NBA", "NCAAB"])
    st.divider()
    if st.button("🔄 RE-SYNC LIVE ODDS", use_container_width=True):
        st.cache_data.clear()
    
    # Check for the correct API Key name in your config
    st.info(f"API Key: {'✅ Active' if config.ODDS_API_KEY else '❌ Missing'}")
    st.caption(f"Last Sync: {datetime.now().strftime('%H:%M:%S')}")

# --- 5. EXECUTION ---
try:
    with st.spinner("Analyzing Market Inefficiencies..."):
        all_edges, analyzer = run_intelligence_engine(sport)
        
        if all_edges:
            top_plays = rank_edges(all_edges, max_plays=5)

            # --- TOP 2 SNIPER PARLAY ---
            if len(top_plays) >= 2:
                p1, p2 = top_plays[0], top_plays[1]
                st.markdown(f"""
                <div class="parlay-card">
                    <h3 style='margin-top:0;'>🔥 THE DAILY SNIPER PARLAY (TOP 2)</h3>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <h4 style='margin:5px 0;'>1. {p1.play_side} {p1.away_team}@{p1.home_team} ({p1.market_spread_home:+.1f})</h4>
                            <h4 style='margin:5px 0;'>2. {p2.play_side} {p2.away_team}@{p2.home_team} ({p2.market_spread_home:+.1f})</h4>
                        </div>
                        <div style='text-align: right;'>
                            <h1 style='margin:0; color: #aff5b4;'>+264</h1>
                            <small>TOTAL EDGE: {round(p1.spread_edge + p2.spread_edge, 1)} PTS</small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # --- MAIN MATRIX & STATS ---
            col_matrix, col_stats = st.columns([3, 1])

            with col_matrix:
                st.subheader("📡 Live Market Edge Matrix")
                df = pd.DataFrame([{
                    "Matchup": f"{e.away_team} @ {e.home_team}",
                    "Side": e.play_side,
                    "Model": e.model_spread_home,
                    "Market": e.market_spread_home,
                    "Edge": e.spread_edge,
                    "Confidence": e.confidence
                } for e in all_edges])
                
                st.dataframe(df.style.background_gradient(subset=['Edge'], cmap='Greens'), 
                             use_container_width=True, hide_index=True)

            with col_stats:
                st.subheader("📊 Tactical Status")
                st.metric("Avg Market Edge", f"{df['Edge'].mean():.1f} pts")
                st.metric("High Conf Plays", len([e for e in all_edges if e.confidence == "HIGH"]))
                
                st.divider()
                st.markdown("**Injury Report**")
                for p in top_plays[:2]:
                    st.caption(f"**{p.home_team}:** {p.injury_summary_home if p.injury_summary_home else 'Clean'}")
        else:
            st.warning("No active edges found for this slate. Check back later!")

except Exception as e:
    st.error(f"Waiting for Data Feed... Error: {e}")
    st.info("Check your Streamlit Secrets for ODDS_API_KEY.")
