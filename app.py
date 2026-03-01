import streamlit as st
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="EDGEINTEL | SYNDICATE", layout="wide")

# -----------------------------
# THEME + DARK BUTTONS
# -----------------------------
st.markdown("""
<style>
    .stApp { background-color: #0D1117 !important; color: #E6E8EE !important; }

    /* Dark, premium buttons */
    div.stButton > button {
        width: 100%;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        background: rgba(255,255,255,0.06) !important;
        color: #E6E8EE !important;
        font-weight: 900 !important;
        padding: 0.6rem 0.9rem !important;
        transition: 120ms ease-in-out;
    }
    div.stButton > button:hover {
        border: 1px solid rgba(0,245,212,0.35) !important;
        background: rgba(0,245,212,0.10) !important;
        transform: translateY(-1px);
    }

    .whale-card {
        background: linear-gradient(135deg, #161B22 0%, #2E1A47 100%);
        border: 1px solid #30363D; border-left: 5px solid #00F5D4;
        border-radius: 14px; padding: 22px; margin-bottom: 20px;
        box-shadow: 0 18px 60px rgba(0,0,0,0.35);
    }

    .sport-header {
        font-size: 0.9rem; font-weight: 950; color: #00F5D4;
        letter-spacing: 2px; text-transform: uppercase;
        border-bottom: 1px solid #30363D; padding-bottom: 8px; margin: 24px 0 14px 0;
    }

    .game-card {
        background: linear-gradient(180deg, #161B22 0%, rgba(22,27,34,0.65) 100%);
        border: 1px solid #30363D;
        border-radius: 12px; padding: 16px; height: 100%;
        box-shadow: 0 12px 40px rgba(0,0,0,0.22);
    }

    .sharp-teal { color: #00F5D4; font-weight: 950; }
    .muted { color: rgba(230,232,238,0.72); }

    .prop-badge {
        display:inline-block;
        background: rgba(0, 245, 212, 0.10); color: #00F5D4;
        padding: 4px 10px; border-radius: 8px; font-size: 0.8rem; font-weight: 900;
        border: 1px solid rgba(0, 245, 212, 0.28);
    }

    .panel {
        background: #0f1520;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 14px 55px rgba(0,0,0,0.35);
    }

    .dossier {
        background: #101826;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 18px 65px rgba(0,0,0,0.40);
    }

    .dossier h4 { margin: 0 0 6px 0; }
    .dline { margin: 6px 0; }
    .tag {
        display:inline-block;
        padding: 3px 9px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.05);
        font-size: 12px;
        font-weight: 900;
        margin-right: 8px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DATA (DEMO BOARD — replace later with live feed)
# -----------------------------
master_data = {
    "NBA": [
        {"game":"76ers @ Celtics","spread":"BOS -9.5","prop":"J. Brown O 27.5 PTS",
         "intel":"DEMO INTEL: usage shift + bench mismatch creates price gap.",
         "drivers":["Usage spike","Bench disparity","Pace edge","Shot quality"],
         "risk":["Late line correction","Blowout minutes","Foul trouble/variance"],
         "invalidate":["Unexpected starter in","Prop line jumps > 1.0","Pace projection flips"]},
        {"game":"Knicks @ Spurs","spread":"SAS -1.5","prop":"Wemby O 4.5 BLK",
         "intel":"DEMO INTEL: rim pressure vs block rate triggers edge.",
         "drivers":["Rim attempts","Block rate matchup","Paint touches"],
         "risk":["Foul trouble","Opp pulls into spacing 5-out"],
         "invalidate":["Minutes restriction","Opp changes shot diet to perimeter"]},
        {"game":"Kings @ Lakers","spread":"LAL -13.0","prop":"Luka O 3.5 3PM",
         "intel":"DEMO INTEL: early usage + perimeter leakage.",
         "drivers":["3PA volume","Defensive leakage","Early game minutes"],
         "risk":["Runaway reduces minutes","Cold shooting variance"],
         "invalidate":["Line moves 1.5+","Minutes limit news"]}
    ],
    "NHL": [
        {"game":"Knights @ Penguins","spread":"VGK ML","prop":"Eichel O 2.5 Shots",
         "intel":"DEMO INTEL: zone time + attempts projection.",
         "drivers":["Shot attempts","O-zone time","Matchup line advantage"],
         "risk":["Early lead slows pace","Goalie variance"],
         "invalidate":["Line scramble / goalie swap"]},
        {"game":"Panthers @ Islanders","spread":"FLA -145","prop":"Barkov 1+ Point",
         "intel":"DEMO INTEL: PP exposure + top line matchup.",
         "drivers":["PP usage","Top line minutes","Possession edge"],
         "risk":["Low-event game","Goalie steal"],
         "invalidate":["Top line shuffle"]},
        {"game":"Flames @ Ducks","spread":"ANA -1.5","prop":"McTavish O 0.5 PTS",
         "intel":"DEMO INTEL: home form + xGF trend.",
         "drivers":["Recent xGF","Home matchup","Finishing volume"],
         "risk":["Empty net variance","Puckline pain"],
         "invalidate":["Back-to-back lineup swing"]}
    ],
    "UFC": [
        {"game":"UFC: Fighter A vs Fighter B","spread":"A -150","prop":"Over 1.5 Rounds",
         "intel":"DEMO INTEL: grappling neutralizes early KO paths; tempo projects longer.",
         "drivers":["Clinch time","Takedown threat","Finish-rate suppression"],
         "risk":["One-shot KO variance","Ref standups"],
         "invalidate":["Short notice injury rumor","Weight cut issues"]},
        {"game":"UFC: Fighter C vs Fighter D","spread":"D +135","prop":"D by Decision",
         "intel":"DEMO INTEL: cardio edge + late rounds scoring bias.",
         "drivers":["Round 3 volume","Control time","Damage differential"],
         "risk":["Judges variability","Early knockdown swings"],
         "invalidate":["Fight camp disruption","Takedown defense collapse"]},
        {"game":"UFC: Fighter E vs Fighter F","spread":"E -110","prop":"E by KO/TKO",
         "intel":"DEMO INTEL: chin mismatch + power differential.",
         "drivers":["Power shots landed","Defense leakage","Distance control"],
         "risk":["Wrestling surprise path","Cardio dump"],
         "invalidate":["Late odds steam against","Style mismatch revealed"]}
    ]
}

# -----------------------------
# SESSION STATE
# -----------------------------
if "selected" not in st.session_state:
    st.session_state.selected = None  # dict
if "chat" not in st.session_state:
    st.session_state.chat = []  # list of {"role","content"}

def analyst_answer(match, question: str) -> str:
    # Deep structured response (stable, deterministic). Swap with real LLM later if you want.
    drivers = "\n".join([f"- {x}" for x in match["drivers"]])
    risks = "\n".join([f"- {x}" for x in match["risk"]])
    invalid = "\n".join([f"- {x}" for x in match["invalidate"]])

    return f"""
**Dossier: {match['game']}**
- Spread: **{match['spread']}**
- Prop: **{match['prop']}**

**Thesis**
{match['intel']}

**Primary Drivers**
{drivers}

**Risk / Variance**
{risks}

**Invalidation Rules (when we pass)**
{invalid}

**Your question**
{question}

**Answer (operator-grade)**
- Translate the question into: *Does it change probability, price, or timing?*
- If it changes probability → adjust confidence/sizing.
- If it changes price → only take if number still beats our threshold.
- If it changes timing → act early or don’t act at all.

If you want, ask: **“Give me the best execution plan + sizing.”**
""".strip()

# -----------------------------
# HEADER
# -----------------------------
st.title("🏛️ EDGEINTEL SYNDICATE")
stamp = datetime.now().strftime("%b %d, %Y • %I:%M %p")
st.markdown(f"""
<div class="panel">
  <span class="tag">MODE: <span class="sharp-teal">DEMO INTEL</span></span>
  <span class="tag">SCAN: <span class="sharp-teal">ACTIVE</span></span>
  <span class="tag">UPDATED: <span class="sharp-teal">{stamp}</span></span>
</div>
""", unsafe_allow_html=True)

# TOP WHALE PLAY
st.markdown("""
<div class="whale-card">
  <div style="color:#00F5D4;font-weight:950;font-size:0.75rem;letter-spacing:2px;">🚨 FEATURED WHALE PLAY</div>
  <h2 style="margin:10px 0;">NBA: 76ERS @ CELTICS</h2>
  <div style="font-size:1.05rem;">
    <b>SPREAD: <span class="sharp-teal">CELTICS -9.5</span></b>
    &nbsp; | &nbsp;
    <b>PROP: <span class="prop-badge">J. BROWN OVER 27.5 PTS</span></b>
    <div class="muted" style="margin-top:8px;">Operator note: edge is thesis + execution. Don’t chase the worst number.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# BOARD
# -----------------------------
for sport, games in master_data.items():
    st.markdown(f'<div class="sport-header">📡 TOP 3 {sport} SLATE</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, g in enumerate(games):
        with cols[i]:
            st.markdown(f"""
            <div class="game-card">
              <div style="font-weight:950;margin-bottom:8px;">{g['game']}</div>
              <div style="margin-bottom:8px;">Spread: <span class="sharp-teal">{g['spread']}</span></div>
              <div style="margin-bottom:10px;"><span class="prop-badge">🔥 {g['prop']}</span></div>
              <div class="muted" style="font-size:12px;line-height:1.45;">{g['intel']}</div>
            </div>
            """, unsafe_allow_html=True)

            # INLINE click handling (no callbacks). This makes clicks feel instant.
            if st.button("SCAN INTEL", key=f"scan_{sport}_{i}"):
                st.session_state.selected = {"sport": sport, **g}
                st.session_state.chat = []  # reset chat per matchup for clarity

# -----------------------------
# DOSSIER + AI CHAT
# -----------------------------
if st.session_state.selected:
    m = st.session_state.selected
    st.markdown("---")
    st.subheader(f"🧠 MATCHUP DOSSIER — {m['sport']} • {m['game']}")

    st.markdown(f"""
    <div class="dossier">
      <h4><span class="sharp-teal">{m['game']}</span></h4>
      <div class="dline">Spread: <b>{m['spread']}</b> &nbsp; | &nbsp; Prop: <b>{m['prop']}</b></div>
      <div class="dline muted">{m['intel']}</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🧠 Explain the edge"):
            q = "Explain the edge like I’m an investor. What’s the real driver?"
            st.session_state.chat.append({"role":"user","content":q})
            st.session_state.chat.append({"role":"assistant","content":analyst_answer(m, q)})
    with c2:
        if st.button("⚠️ What could kill it?"):
            q = "What are the top 3 ways this play fails and how do we defend?"
            st.session_state.chat.append({"role":"user","content":q})
            st.session_state.chat.append({"role":"assistant","content":analyst_answer(m, q)})
    with c3:
        if st.button("🎯 Execution + sizing"):
            q = "Give me execution timing + sizing rules + what number I refuse to take."
            st.session_state.chat.append({"role":"user","content":q})
            st.session_state.chat.append({"role":"assistant","content":analyst_answer(m, q)})

    st.markdown("### Ask SCOTTY")
    user_msg = st.chat_input("Ask a question about this matchup… (sizing, invalidation, props, hedges, scenarios)")
    if user_msg:
        st.session_state.chat.append({"role":"user","content":user_msg})
        st.session_state.chat.append({"role":"assistant","content":analyst_answer(m, user_msg)})

    for msg in st.session_state.chat[-12:]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

st.divider()
st.link_button("🚀 UNLOCK FULL SYNDICATE ACCESS", "https://whop.com/YOUR_LINK", use_container_width=True)
