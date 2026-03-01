import streamlit as st
from datetime import datetime

st.set_page_config(page_title="EDGEINTEL | SYNDICATE", layout="wide")

# -----------------------------
# THEME + DARK BUTTONS + CLEAN LAYOUT
# -----------------------------
st.markdown("""
<style>
  .stApp { background-color: #0D1117 !important; color: #E6E8EE !important; }
  header{ visibility:hidden; }

  /* Buttons */
  div.stButton > button {
      width: 100%;
      border-radius: 12px !important;
      border: 1px solid rgba(255,255,255,0.10) !important;
      background: rgba(255,255,255,0.05) !important;
      color: #E6E8EE !important;
      font-weight: 900 !important;
      padding: 0.55rem 0.9rem !important;
      transition: 140ms ease-in-out;
  }
  div.stButton > button:hover {
      border: 1px solid rgba(0,245,212,0.35) !important;
      background: rgba(0,245,212,0.10) !important;
      transform: translateY(-1px);
  }

  .panel {
      background: #0f1520;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 14px;
      padding: 14px;
      box-shadow: 0 14px 55px rgba(0,0,0,0.35);
  }
  .card {
      background: linear-gradient(180deg, #161B22 0%, rgba(22,27,34,0.65) 100%);
      border: 1px solid #30363D;
      border-radius: 12px;
      padding: 14px;
      box-shadow: 0 10px 36px rgba(0,0,0,0.22);
  }

  .sport {
      font-size: 0.82rem; font-weight: 950; color: #00F5D4;
      letter-spacing: 2px; text-transform: uppercase;
      border-bottom: 1px solid #30363D; padding-bottom: 8px; margin: 18px 0 12px 0;
  }

  .teal { color: #00F5D4; font-weight: 950; }
  .muted { color: rgba(230,232,238,0.72); }

  .pill {
      display:inline-block;
      padding: 5px 10px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 900;
      border: 1px solid rgba(255,255,255,0.12);
      background: rgba(255,255,255,0.04);
      margin-right: 8px;
  }

  .kpi {
      display:flex; gap:10px; flex-wrap:wrap;
      margin-top: 8px;
  }

  .sectionTitle {
      font-weight: 950;
      margin: 8px 0 6px 0;
  }

  .list {
      margin: 0;
      padding-left: 18px;
  }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DATA (DEMO)
# -----------------------------
master_data = {
    "NBA": [
        {"game":"76ers @ Celtics","spread":"BOS -9.5","prop":"J. Brown O 27.5 PTS",
         "thesis":"Usage shift + bench mismatch creates a misprice.",
         "drivers":["Secondary usage consolidates into primary scorer props","Opponent depth drop-off","Shot quality profile improves"],
         "risk":["Late lineup reversal","Blowout reduces 4Q minutes","Foul trouble variance"],
         "invalidate":["Key starter returns unexpectedly","Prop moves > 1.0 against us","Pace projection flips"],
         "execution":"Take early. If number worsens, reduce size or pass. Do not chase."},
        {"game":"Knicks @ Spurs","spread":"SAS -1.5","prop":"Wemby O 4.5 BLK",
         "thesis":"Rim pressure meets elite block profile.",
         "drivers":["Opponent rim attempts","Block rate matchup","Paint touch volume"],
         "risk":["Foul trouble","Opponent goes 5-out to avoid rim"],
         "invalidate":["Minutes restriction news","Opponent shot diet shifts perimeter-heavy"],
         "execution":"Prefer live entry if early foul risk shows; otherwise pregame small."},
        {"game":"Kings @ Lakers","spread":"LAL -13.0","prop":"Luka O 3.5 3PM",
         "thesis":"Perimeter leakage + early usage supports 3PM.",
         "drivers":["3PA volume","Defensive leakage","Early rotation minutes"],
         "risk":["Runaway reduces minutes","Cold shooting variance"],
         "invalidate":["Minutes limit","Line/prop moves sharply"],
         "execution":"Target best number; don’t pay premium for a public prop."}
    ],
    "NHL": [
        {"game":"Knights @ Penguins","spread":"VGK ML","prop":"Eichel O 2.5 Shots",
         "thesis":"Zone time + attempts projection supports shot prop.",
         "drivers":["Shot attempts","O-zone time","Line matchup advantage"],
         "risk":["Early lead slows pace","Goalie variance"],
         "invalidate":["Goalie swap","Line shuffle reduces ice time"],
         "execution":"If VGK scores early, consider live under on pace; otherwise hold."},
        {"game":"Panthers @ Islanders","spread":"FLA -145","prop":"Barkov 1+ Point",
         "thesis":"Top line exposure + PP usage gives value.",
         "drivers":["PP time","Top line minutes","Possession edge"],
         "risk":["Low-event game","Goalie steal"],
         "invalidate":["Top line reshuffle","PP unit change"],
         "execution":"Take 1+ point if price stable; avoid juiced alt lines."},
        {"game":"Flames @ Ducks","spread":"ANA -1.5","prop":"McTavish O 0.5 PTS",
         "thesis":"Home form + xGF trend supports points prop.",
         "drivers":["Recent xGF","Home matchup","Volume + finishing"],
         "risk":["Empty net variance","Puckline pain"],
         "invalidate":["Back-to-back lineup swing","Star scratched"],
         "execution":"Points prop is cleaner than puckline unless number is great."}
    ],
    "UFC": [
        {"game":"UFC: Fighter A vs Fighter B","spread":"A -150","prop":"Over 1.5 Rounds",
         "thesis":"Grappling threat suppresses early finish paths.",
         "drivers":["Clinch time projection","Takedown attempts","Finish-rate suppression"],
         "risk":["One-shot KO variance","Ref standups alter control"],
         "invalidate":["Weight cut issues","Short-notice injury rumor"],
         "execution":"If live shows early grappling success, add small; otherwise keep base."},
        {"game":"UFC: Fighter C vs Fighter D","spread":"D +135","prop":"D by Decision",
         "thesis":"Cardio edge + late scoring bias favors decision path.",
         "drivers":["Round 3 volume","Control time","Damage differential trend"],
         "risk":["Judges variability","Early knockdown swings"],
         "invalidate":["Camp disruption","Takedown defense collapse"],
         "execution":"Decision props are fragile—cap size and avoid bad price."},
        {"game":"UFC: Fighter E vs Fighter F","spread":"E -110","prop":"E by KO/TKO",
         "thesis":"Chin mismatch + power differential is the trigger.",
         "drivers":["Power shots landed","Defense leakage","Distance control"],
         "risk":["Wrestling surprise path","Cardio dump"],
         "invalidate":["Late steam against","Style mismatch revealed"],
         "execution":"Only take if price stays near open. Don’t buy inflated KO."}
    ]
}

# -----------------------------
# STATE
# -----------------------------
if "selected" not in st.session_state:
    st.session_state.selected = None
if "chat" not in st.session_state:
    st.session_state.chat = []

def select_matchup(sport, g):
    st.session_state.selected = {"sport": sport, **g}
    st.session_state.chat = []

def scotty_answer(m, q):
    return f"""
**Active Target:** {m['sport']} • {m['game']}

**Thesis:** {m['thesis']}

**Answer to your question:** {q}

**Decision Logic**
- If it changes **probability** → adjust confidence/sizing
- If it changes **price** → only take if number is still +EV
- If it changes **timing** → act early or pass

**Execution Rule:** {m['execution']}
""".strip()

# -----------------------------
# HEADER
# -----------------------------
st.title("🏛️ EDGEINTEL SYNDICATE")
stamp = datetime.now().strftime("%b %d, %Y • %I:%M %p")
st.markdown(f"""
<div class="panel">
  <span class="pill">MODE: <span class="teal">DEMO INTEL</span></span>
  <span class="pill">SCAN: <span class="teal">ACTIVE</span></span>
  <span class="pill">UPDATED: <span class="teal">{stamp}</span></span>
  <span class="pill">FLOW: <span class="teal">SELECT → DOSSIER → CHAT</span></span>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# MAIN LAYOUT: LEFT BOARD | RIGHT DOSSIER
# -----------------------------
left, right = st.columns([1.05, 1.15], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### 🎯 Board (Click a matchup)")
    for sport, games in master_data.items():
        st.markdown(f'<div class="sport">{sport}</div>', unsafe_allow_html=True)
        for i, g in enumerate(games):
            st.markdown(f"""
            <div class="card" style="margin-bottom:10px;">
              <div style="font-weight:950;">{g['game']}</div>
              <div class="muted" style="margin-top:6px;">
                Spread: <span class="teal">{g['spread']}</span> &nbsp; | &nbsp;
                Prop: <span class="teal">{g['prop']}</span>
              </div>
              <div class="muted" style="margin-top:6px; font-size:12px;">{g['thesis']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("SCAN INTEL", key=f"scan_{sport}_{i}"):
                select_matchup(sport, g)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("### 🧠 Dossier + Scotty (AI)")

    if not st.session_state.selected:
        st.info("Select a matchup on the left. The dossier and AI chat will load here.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        m = st.session_state.selected

        st.markdown(f"""
        <div class="card">
          <div style="font-weight:950; font-size:16px;">
            <span class="teal">{m['sport']}</span> • {m['game']}
          </div>
          <div class="kpi">
            <span class="pill">SPREAD: <span class="teal">{m['spread']}</span></span>
            <span class="pill">PROP: <span class="teal">{m['prop']}</span></span>
          </div>
          <div class="muted" style="margin-top:10px;"><b>Thesis:</b> {m['thesis']}</div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Thesis", "Drivers", "Risk", "Invalidation", "Execution"])

        with tab1:
            st.markdown("**One-line thesis:**")
            st.markdown(f"- {m['thesis']}")

        with tab2:
            st.markdown("**Primary drivers:**")
            st.markdown("<ul class='list'>" + "".join([f"<li>{x}</li>" for x in m["drivers"]]) + "</ul>", unsafe_allow_html=True)

        with tab3:
            st.markdown("**What can kill it:**")
            st.markdown("<ul class='list'>" + "".join([f"<li>{x}</li>" for x in m["risk"]]) + "</ul>", unsafe_allow_html=True)

        with tab4:
            st.markdown("**Pass rules:** (if any of these happen, we do NOT bet)")
            st.markdown("<ul class='list'>" + "".join([f"<li>{x}</li>" for x in m["invalidate"]]) + "</ul>", unsafe_allow_html=True)

        with tab5:
            st.markdown("**Execution plan:**")
            st.markdown(f"- {m['execution']}")

        st.markdown("---")
        st.markdown("#### Ask Scotty")
        sug1, sug2, sug3 = st.columns(3)
        if sug1.button("Explain edge like investor"):
            q = "Explain the edge like I'm an investor. What matters most?"
            st.session_state.chat.append({"role":"user","content":q})
            st.session_state.chat.append({"role":"assistant","content":scotty_answer(m, q)})
        if sug2.button("What would invalidate it?"):
            q = "What specifically would invalidate this edge?"
            st.session_state.chat.append({"role":"user","content":q})
            st.session_state.chat.append({"role":"assistant","content":scotty_answer(m, q)})
        if sug3.button("Sizing + timing rules"):
            q = "Give sizing and timing rules. When do we pass?"
            st.session_state.chat.append({"role":"user","content":q})
            st.session_state.chat.append({"role":"assistant","content":scotty_answer(m, q)})

        user_msg = st.chat_input("Ask about this matchup (props, spread, scenarios, sizing, hedges)…")
        if user_msg:
            st.session_state.chat.append({"role":"user","content":user_msg})
            st.session_state.chat.append({"role":"assistant","content":scotty_answer(m, user_msg)})

        for msg in st.session_state.chat[-12:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.link_button("🚀 UNLOCK FULL SYNDICATE ACCESS", "https://whop.com/YOUR_LINK", use_container_width=True)
