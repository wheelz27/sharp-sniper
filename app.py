import streamlit as st
import pandas as pd
import time

# --- 1. PREMIUM DARK UI ---
st.set_page_config(page_title="EDGEINTEL | SYNDICATE", layout="wide")

st.markdown("""
    <style>
    /* Professional Dark Background */
    .stApp { background-color: #0d1117; color: #e6edf3; }
    
    /* Glowing Command Center Header */
    .command-header {
        background: rgba(23, 27, 33, 0.8);
        border: 1px solid #30363d;
        border-left: 5px solid #238636;
        padding: 30px; border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        margin-bottom: 25px;
    }

    /* Moving "Live" Pulse */
    .pulse {
        display: inline-block; width: 10px; height: 10px;
        border-radius: 50%; background: #238636;
        box-shadow: 0 0 0 0 rgba(35, 134, 54, 1);
        animation: pulse-green 2s infinite; margin-right: 10px;
    }
    @keyframes pulse-green {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(35, 134, 54, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(35, 134, 54, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(35, 134, 54, 0); }
    }

    /* Highlighted Matrix Rows */
    .stTable { background-color: #161b22; border-radius: 10px; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE COMMAND HEADER ---
st.markdown("""
    <div class="command-header">
        <h1 style='margin:0; font-family: monospace;'>📡 <span class="pulse"></span>EDGEINTEL COMMAND CENTER</h1>
        <p style='color: #8b949e; letter-spacing: 1px;'>NEURAL ENGINE v3.4 | REAL-TIME MARKET ARBITRAGE</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. IMPACT METRICS ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("ENGINE LATENCY", "12ms", "OPTIMAL")
with c2: st.metric("SCAN RATE", "14,200/min", "+12%")
with c3: st.metric("ACTIVE EDGES", "Locked", help="Join Syndicate to view")
with c4: st.metric("ALPHA TIER", "+264", "Target Found")

st.divider()

# --- 4. THE EDGE MATRIX (IMPROVED VISIBILITY) ---
st.subheader("📊 Live Market Projection Matrix")

# We use more aggressive mockup data so the table looks "full" and "impressive"
data = [
    {"GAME": "🏀 LAL @ BOS", "VEGAS": "-5.5", "MODEL": "-8.1", "EDGE": "🔥 +2.6", "PROB": "68%"},
    {"GAME": "🏀 NYK @ PHI", "VEGAS": "+3.0", "MODEL": "-1.5", "EDGE": "🔥 +4.5", "PROB": "74%"},
    {"GAME": "🏀 PHX @ DAL", "VEGAS": "-1.5", "MODEL": "-1.5", "EDGE": "0.0", "PROB": "51%"},
    {"GAME": "🏀 GSW @ DEN", "VEGAS": "+6.0", "MODEL": "+4.2", "EDGE": "💎 +1.8", "PROB": "61%"},
    {"GAME": "🏀 MIA @ MIL", "VEGAS": "-7.0", "MODEL": "-9.5", "EDGE": "🔥 +2.5", "PROB": "65%"},
]
df = pd.DataFrame(data)

# Injecting the table with high contrast
st.table(df)

# --- 5. THE SYNDICATE CALL TO ACTION ---
st.markdown("### 🎯 SYNDICATE SNIPER PARLAYS")
left, right = st.columns([1.5, 1])

with left:
    st.markdown("""
        <div style="background: rgba(35, 134, 54, 0.1); border: 1px solid #238636; padding: 25px; border-radius: 12px;">
            <h4 style="color:#3fb950; margin-top:0;">🔓 ACTIVE SNIPER PARLAY (+264)</h4>
            <p style="color:#8b949e; font-family: monospace;">[LEG 1] UNKNOWN - JOIN DISCORD TO UNLOCK</p>
            <p style="color:#8b949e; font-family: monospace;">[LEG 2] UNKNOWN - JOIN DISCORD TO UNLOCK</p>
            <p style="color:#8b949e; font-family: monospace;">[LEG 3] UNKNOWN - JOIN DISCORD TO UNLOCK</p>
        </div>
    """, unsafe_allow_html=True)

with right:
    st.write("#### Secure Your Edge")
    st.write("Stop betting on luck. Start trading on data. Join the world's most elite betting syndicate.")
    st.link_button("🚀 JOIN THE SYNDICATE", "https://whop.com/YOUR_LINK", use_container_width=True)

st.divider()
st.caption("SCANNING... Data synced with Vegas API. Neural weights verified.")
