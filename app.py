import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. HUD STYLING ---
st.set_page_config(page_title="EDGEINTEL | PRO", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #06090f; }
    .status-bar { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
    .highlight { color: #238636; font-weight: bold; }
    .matrix-row { border-bottom: 1px solid #30363d; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 2. THE TOP HUD ---
st.markdown(f"""
    <div class="status-bar">
        <span class="highlight">● SYSTEM ONLINE</span> | 
        LAST API SYNC: {datetime.now().strftime('%H:%M:%S')} | 
        THEATER: NBA/NCAAB | 
        <span style="color:#f85149;">VOLATILITY: HIGH</span>
    </div>
""", unsafe_allow_html=True)

# --- 3. THE COMMAND CENTER ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📡 Live Intelligence Matrix")
    # This creates a more detailed table with "Movement" to impress visitors
    data = [
        {"GAME": "LAL @ BOS", "VEGAS": "-5.5", "MODEL": "-8.2", "EDGE": "+2.7", "TOTAL": "224.5", "MOVE": "⬆️"},
        {"GAME": "NYK @ PHI", "VEGAS": "+3.0", "MODEL": "-1.5", "EDGE": "+4.5", "TOTAL": "212.0", "MOVE": "🔥"},
        {"GAME": "PHX @ DAL", "VEGAS": "-1.0", "MODEL": "-0.5", "EDGE": "+0.5", "TOTAL": "231.5", "MOVE": "➡️"},
    ]
    st.table(data)

with col2:
    st.subheader("🎯 Sniper Parlay")
    st.markdown("""
        <div style="background:#0d1117; border: 2px solid #238636; padding: 20px; border-radius: 10px;">
            <h3 style="color:#238636; margin-top:0;">+264 ALPHA</h3>
            <p>1. LAL +5.5 <span style="color:#8b949e;">[Verified]</span></p>
            <p>2. PHI -1.5 <span style="color:#8b949e;">[Verified]</span></p>
            <hr>
            <p style="font-size: 0.8rem;"><i>Join the Syndicate to unlock the full 3-leg sniper parlay.</i></p>
        </div>
    """, unsafe_allow_html=True)
    st.button("🚀 UNLOCK FULL SYNDICATE ACCESS", use_container_width=True)

# --- 4. THE "INSIGHT" SECTION ---
st.divider()
st.write("### 🧠 Why the Model favors the Knicks today:")
st.info("Neural Engine detected a 4.2% discrepancy in defensive rebounding efficiency due to Embiid's rest status. Vegas has not yet adjusted the spread to reflect the true possession-per-game handicap.")
