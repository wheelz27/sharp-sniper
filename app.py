import streamlit as st

# --- 1. 2026 CLUBROOM CONTRAST THEME ---
st.set_page_config(page_title="EDGEINTEL | PRO", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0A0C10 !important; color: #E9EEF5 !important; }
    
    /* Syndicate Whale Card */
    .whale-card {
        background: linear-gradient(145deg, #161B22, #0A0C10);
        border: 1px solid #1f242d;
        border-left: 4px solid #40E0FF;
        border-radius: 8px; padding: 25px; margin-bottom: 35px;
    }

    /* Sport Headers */
    .sport-header {
        background-color: #161B22; border-left: 3px solid #40E0FF;
        padding: 8px 15px; margin: 25px 0 10px 0;
        font-weight: 700; color: #40E0FF;
        text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1.5px;
    }

    .sharp-blue { color: #40E0FF; font-weight: 700; }
    .muted-intel { color: #9BA3AF; font-size: 0.9rem; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# --- 2. MASTER SYNDICATE DATA (LIVE MARCH 1, 2026) ---
master_data = {
    "NBA: 76ers @ Celtics": {"status": "8:00 PM ET", "edge": "BOS -9.5", "intel": "Joel Embiid (Oblique) is officially OUT. Celtics missing Tatum (Achilles), but Jaylen Brown is averaging 29.1 PPG as the solo engine. Boston’s bench is #2 in Net Rating; Philly’s is bottom-5. Lay the points."},
    "NBA: Bucks @ Bulls": {"status": "LIVE (Q4)", "edge": "CHI +6.5", "intel": "Giannis (Calf) is OUT. MIL offensive rating drops 11.4 points without him. Bulls keeping it close at 74-76. Sharp money is on the Bulls spread to hold at home."},
    "NBA: Kings @ Lakers": {"status": "9:30 PM ET", "edge": "LAL -13.0", "intel": "Luka Doncic and LeBron James (Foot Management) both ACTIVE. Kings are missing Sabonis and Zach LaVine. Absolute mismatch in transition volume. Lakers blowout expected."},
    "NHL: Panthers @ Islanders": {"status": "6:30 PM ET", "edge": "FLA ML", "intel": "NYI are 1-7 in home openers following long breaks (Olympic rest). Florida returns 100% healthy with Kulikov back. Huge edge in expected goals (xG)."},
    "MLS: Orlando @ Miami": {"status": "7:00 PM ET", "edge": "MIA ML", "intel": "The Florida Derby. Messi and Suarez are starting. Miami seeking their first goal of 2026 after the LAFC shutout. Orlando missing key CB Jansson."},
    "CBB: #8 Purdue @ Ohio State": {"status": "FINAL", "edge": "PURDUE -6.5", "intel": "WIN. Purdue survived the Buckeyes 76-74. While they didn't cover the full 6.5, the moneyline 'Whale' play hit for the Syndicate."}
}

# --- 3. THE WHALE (MAX UNIT PLAY) ---
st.markdown("""
<div class="whale-card">
    <div style="color: #40E0FF; font-weight: 800; font-size: 0.7rem; letter-spacing: 1.5px; margin-bottom:10px;">🚨 MAX UNIT SYNDICATE PLAY</div>
    <h2 style="margin: 0;">PHILADELPHIA 76ers @ BOSTON CELTICS</h2>
    <p style="font-size: 1.2rem; margin: 5px 0;"><b>VERDICT: <span class="sharp-blue">CELTICS -9.5</span></b></p>
    <p class="muted-intel">
        <b>SHARP LOGIC:</b> Market hasn't adjusted to the bench disparity. With Embiid and Paul George out, Philly loses 42% of their scoring volume. 
        Boston's second unit (Pritchard/White) vs Philly's G-League caliber depth is the deciding factor.
    </p>
</div>
""", unsafe_allow_html=True)

# --- 4. ON-DEMAND DEEP SCAN (THE DROP-DOWN) ---
st.subheader("🎯 ON-DEMAND SYSTEM SCAN")
selected_match = st.selectbox("SEARCH SUNDAY SLATE:", list(master_data.keys()))

if selected_match:
    d = master_data[selected_match]
    st.markdown(f"""
    <div style="background:#161B22; padding:20px; border-radius:8px; border-top:2px solid #40E0FF; margin-top:10px;">
        <h3 style="margin-top:0;">{selected_match.upper()}</h3>
        <p><b>SYSTEM VERDICT: <span class="sharp-blue">{d['edge']}</span></b> | <b>STATUS:</b> {d['status']}</p>
        <p class="muted-intel"><b>SYNDICATE INTEL:</b> {d['intel']}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. GLOBAL RADAR OVERVIEW ---
st.markdown('<div class="sport-header">📡 GLOBAL RADAR OVERVIEW</div>', unsafe_allow_html=True)

for cat in ["NBA", "NHL", "MLS", "CBB"]:
    st.write(f"#### {cat} SUNDAY SLATE")
    for game, info in master_data.items():
        if game.startswith(cat):
            c1, c2, c3 = st.columns([2, 1, 1])
            c1.markdown(f"**{game.split(': ')[1]}**")
            c2.write(f"{info['status']}")
            c3.markdown(f"<span class='sharp-blue'>{info['edge']}</span>", unsafe_allow_html=True)
    st.divider()

st.link_button("🚀 UNLOCK FULL SYNDICATE ACCESS", "https://whop.com/YOUR_LINK", use_container_width=True)
