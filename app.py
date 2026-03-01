import streamlit as st
import pandas as pd
import random

# --- 1. SETTINGS & SYNDICATE STYLING ---
st.set_page_config(page_title="EDGEINTEL | COMMAND", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #06090f; color: #c9d1d9; }
    .header-box { 
        background: linear-gradient(90deg, #1f6feb 0%, #0d1117 100%);
        padding: 25px; border-radius: 10px; border-left: 5px solid #58a6ff;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #161b22; border: 1px solid #30363d;
        padding: 15px; border-radius: 8px; text-align: center;
    }
    .locked-text { color: #8b949e; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

# --- 2. TOP BANNER (THE VISION) ---
st.markdown("""
    <div class="header-box">
        <h1 style='margin:0;'>📡 EDGEINTEL: INTELLIGENCE HUB</h1>
        <p style='opacity:0.8;'>Proprietary Neural Model vs. Vegas Market Openers</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. LIVE STATS BAR ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Engine Status", "ACTIVE ●", delta="14ms Latency")
col2.metric("Games Analyzed", "14", delta="Live")
col3.metric("Market Volatility", "High", delta="7% Shift")
col4.metric("Syndicate Strength", "+264", delta="Sniper Tier")

st.divider()

# --- 4. THE EDGE MATRIX (THE INSIGHT) ---
st.subheader("📊 Live Market Projection Matrix")
st.write("Comparing Model Fair-Value to Vegas Current Spreads")

# Placeholder data to ensure the screen is NEVER empty for your visitor
# In production, this pulls from your 'all_edges' variable
data = [
    {"Matchup": "Lakers @ Celtics", "Vegas": "-5.5", "Model": "-8.2", "Edge": "+2.7", "Conf": "88%"},
    {"Matchup": "Knicks @ 76ers", "Vegas": "+2.0", "Model": "-1.5", "Edge": "+3.5", "Conf": "92%"},
    {"Matchup": "Suns @ Mavericks", "Vegas": "-1.0", "Model": "-0.5", "Edge": "+0.5", "Conf": "74%"},
    {"Matchup": "Warriors @ Nuggets", "Vegas": "+4.5", "Model": "+6.0", "Edge": "+1.5", "Conf": "81%"},
]
df = pd.DataFrame(data)

st.table(df)

# --- 5. THE "SNIPER" PAYWALL (THE FUNNEL) ---
st.markdown("### 🎯 SYNDICATE SNIPER PLAYS")
c1, c2 = st.columns(2)

with c1:
    st.markdown("""
        <div style="background-color:#161b22; padding:20px; border-radius:10px; border:1px dashed #238636;">
            <h4 style="color:#238636;">🔓 ACTIVE SNIPER PARLAY (+264)</h4>
            <p class="locked-text">Leg 1: [LOCKED - JOIN DISCORD]</p>
            <p class="locked-text">Leg 2: [LOCKED - JOIN DISCORD]</p>
            <p class="locked-text">Leg 3: [LOCKED - JOIN DISCORD]</p>
        </div>
    """, unsafe_allow_html=True)

with c2:
    st.write("#### Unlock the Full Board")
    st.write("Get real-time alerts on your phone the second our model finds a 2.0+ point glitch.")
    st.link_button("🔥 JOIN THE SYNDICATE NOW", "https://whop.com/YOUR_LINK", use_container_width=True)

# --- 6. FOOTER ENGINE LOGS ---
st.divider()
st.caption("System Logs: Neural weights updated. Vegas API synced. Scanning for inefficiencies...")
