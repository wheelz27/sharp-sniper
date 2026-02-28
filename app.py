import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- 1. SETTINGS & PREMIUM STYLING ---
st.set_page_config(page_title="EDGEINTEL | SYNDICATE", layout="wide", page_icon="🎯")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .funnel-box { 
        background: linear-gradient(135deg, #1f6feb 0%, #0d1117 100%);
        padding: 40px; border-radius: 15px; border: 1px solid #388bfd; text-align: center;
        margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .join-btn {
        background-color: #238636; color: white !important; padding: 16px 32px;
        text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;
        font-size: 1.2rem; transition: 0.3s;
    }
    .join-btn:hover { background-color: #2ea043; transform: scale(1.05); }
    .matrix-header { color: #58a6ff; font-family: monospace; letter-spacing: 2px; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE SALES FUNNEL (THE HOOK) ---
st.markdown("""
    <div class="funnel-box">
        <h1 style='margin-top:0;'>🎯 UNLOCK THE SNIPER SYNDICATE</h1>
        <p style='font-size: 1.3rem; opacity: 0.9;'>Automated +264 Parlay Alerts sent to your phone via Private Discord.</p>
        <br>
        <a href="YOUR_PAYMENT_OR_DISCORD_LINK_HERE" class="join-btn">JOIN THE SYNDICATE — GET THE EDGE</a>
    </div>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("🕹️ COMMAND CENTER")
    sport = st.radio("Active Theater", ["NBA", "NCAAB"])
    st.divider()
    
    # This button manually triggers the "Captain Hook" for you
    if st.button("🚀 TEST DISCORD PUSH", use_container_width=True):
        webhook_url = st.secrets.get("DISCORD_WEBHOOK_URL")
        if webhook_url:
            test_payload = {"content": "🎯 **EdgeIntel Alert:** High-value edges detected. Check the Syndicate channel!"}
            requests.post(webhook_url, json=test_payload)
            st.success("Test Alert Sent!")
        else:
            st.error("Missing Webhook URL in Secrets!")

    st.info(f"System Status: ● LIVE")
    st.caption(f"Last Scan: {datetime.now().strftime('%H:%M:%S')}")

# --- 4. THE INTELLIGENCE ENGINE (THE PROOF) ---
st.markdown("<h3 class='matrix-header'>📡 LIVE MARKET INTELLIGENCE</h3>", unsafe_allow_html=True)

try:
    # Importing your backend logic
    from engine.matchups import MatchupAnalyzer
    
    with st.spinner("Analyzing Market Inefficiencies..."):
        analyzer = MatchupAnalyzer(sport=sport.lower())
        all_edges = analyzer.compute_all_edges()

        if all_edges:
            # Displaying the "Why" (Model vs Vegas) to prove it works
            df = pd.DataFrame([{
                "MATCHUP": f"{e.away_team} @ {e.home_team}",
                "VEGAS LINE": f"{e.market_spread_home:+.1f}",
                "OUR MODEL": f"{e.model_spread_home:+.1f}",
                "THE EDGE": f"{e.spread_edge:+.1f} PTS",
                "CONFIDENCE": f"{e.confidence}%"
            } for e in all_edges[:5]]) # Show only top 5 as a free sample
            
            st.table(df)
            st.markdown("---")
            st.write("🔒 *Additional 10+ edges and Sniper Parlays are locked. Join the Syndicate to unlock.*")
        else:
            # This is what you see when lines aren't out yet
            st.info("Market is currently updating. New edges populate as Vegas releases lines.")

except Exception as e:
    st.error(f"Engine connection standby. Error: {e}")
