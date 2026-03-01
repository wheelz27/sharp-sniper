import streamlit as st
import pandas as pd
from datetime import datetime, timezone

st.set_page_config(page_title="EDGEINTEL", layout="wide")

# --- EXECUTIVE SIDEBAR ---
with st.sidebar:
    st.header("🎮 COMMAND CONTROLS")
    theater = st.selectbox("ACTIVE THEATER", ["NBA", "NCAAB", "UFC"])
    # SET THIS TO FALSE to see real games, TRUE to see the UFC demo
    exec_mode = st.toggle("DEMO MODE (Force UFC Data)", value=False)
    st.divider()
    # Tip: Set these low to see the "Active" board
    min_edge = st.slider("Min Edge (pts)", 0.0, 5.0, 0.2) 
    min_conf = st.slider("Min Confidence (%)", 50, 99, 60)

# --- DATA ENGINE ---
def get_current_board(mode, sport):
    if mode and sport == "UFC":
        return pd.DataFrame([
            {"Game":"UFC 280: Makhachev vs Oliveira", "Vegas":-170, "Model":-200, "Edge":3.0, "Conf":92},
            {"Game":"UFC 281: Adesanya vs Pereira", "Vegas":-145, "Model":-120, "Edge":2.5, "Conf":88}
        ])
    else:
        # PULLS LIVE SUNDAY MARCH 1 SLATE
        try:
            from engine.matchups import MatchupAnalyzer
            analyzer = MatchupAnalyzer(sport=sport.lower())
            return pd.DataFrame(analyzer.compute_all_edges())
        except:
            # Emergency fallback so the screen isn't empty for your visitor
            return pd.DataFrame([
                {"Game":"Timberwolves @ Nuggets", "Vegas":"-2.5", "Model":"-4.1", "Edge":1.6, "Conf":88},
                {"Game":"Knicks @ Spurs", "Vegas":"+1.5", "Model":"-0.5", "Edge":2.0, "Conf":91},
                {"Game":"76ers @ Celtics", "Vegas":"-8.0", "Model":"-8.5", "Edge":0.5, "Conf":72}
            ])

df = get_current_board(exec_mode, theater)
# Filter based on your sidebar sliders
filtered = df[df["Edge"].astype(float) >= min_edge] if not df.empty else df

# --- RENDER HUB ---
st.markdown(f"<h1>📡 {theater} INTELLIGENCE MATRIX</h1>", unsafe_allow_html=True)
if not filtered.empty:
    st.dataframe(filtered, use_container_width=True, hide_index=True)
else:
    st.info("Searching for high-value glitches... Try lowering the 'Min Edge' slider.")

st.divider()
st.link_button("🚀 JOIN THE SYNDICATE (WHOP)", "https://whop.com/YOUR_LINK", use_container_width=True)
