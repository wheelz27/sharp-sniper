import os
import streamlit as st
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(page_title="EDGEINTEL | Control Panel", layout="wide")

# ============================================================
# OPTIONAL PASSCODE GATE (NO SIGNUP)
# - If DEMO_PASS is NOT set: app is open to anyone with the URL
# - If DEMO_PASS is set: viewers must enter passcode
# ============================================================
DEMO_PASS = os.getenv("DEMO_PASS", "").strip()
if DEMO_PASS:
    if "access_ok" not in st.session_state:
        st.session_state.access_ok = False

    if not st.session_state.access_ok:
        st.markdown("## 🔒 Access Required")
        st.caption("Enter the access code. No account needed.")
        code = st.text_input("Access code", type="password")
        if st.button("Enter"):
            st.session_state.access_ok = (code.strip() == DEMO_PASS)
        if not st.session_state.access_ok:
            st.stop()

# ============================================================
# THEME (dark SaaS)
# ============================================================
st.markdown("""
<style>
  .stApp { background-color: #0b1220 !important; color: #E6E8EE !important; }
  header{ visibility:hidden; }

  section[data-testid="stSidebar"]{
    background: #0a101b !important;
    border-right: 1px solid rgba(255,255,255,0.06);
  }

  /* Buttons (dark) */
  div.stButton > button {
    border-radius: 10px !important;
    border: 1px solid rgba(120,180,255,0.20) !important;
    background: rgba(120,180,255,0.10) !important;
    color: #E6E8EE !important;
    font-weight: 850 !important;
    padding: 0.42rem 0.75rem !important;
    transition: 120ms ease-in-out;
    width: 100%;
  }
  div.stButton > button:hover {
    border: 1px solid rgba(120,180,255,0.35) !important;
    background: rgba(120,180,255,0.14) !important;
    transform: translateY(-1px);
  }

  .topbar {
    padding: 14px 16px;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(120,180,255,0.10), rgba(0,0,0,0.0));
    box-shadow: 0 18px 60px rgba(0,0,0,0.35);
    margin-bottom: 14px;
  }
  .title { font-size: 18px; font-weight: 950; letter-spacing: 0.3px; }
  .subtitle { font-size: 12px; opacity: 0.78; margin-top: 2px; }

  .pill {
    display:inline-block;
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 950;
    border: 1px solid rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.06);
    color: rgba(230,232,238,0.86);
  }

  .badge {
    display:inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 950;
    border: 1px solid rgba(0,245,212,0.22);
    background: rgba(0,245,212,0.08);
    color: rgba(230,232,238,0.92);
  }

  .rowItem {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap: 12px;
    padding: 10px 12px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.03);
    margin-bottom: 10px;
  }
  .rowLeft { display:flex; align-items:center; gap: 10px; min-width: 260px; }
  .ico {
    width: 30px; height: 30px;
    border-radius: 9px;
    display:flex; align-items:center; justify-content:center;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.04);
    font-weight: 950;
  }
  .rowTitle { font-weight: 900; }
  .rowMeta { font-size: 12px; opacity: 0.78; margin-top: 2px; }
  .muted { opacity: 0.72; }
  .teal { color: #00F5D4; font-weight: 950; }

  .detail {
    padding: 14px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.03);
    box-shadow: 0 18px 60px rgba(0,0,0,0.35);
  }

  .card {
    padding: 12px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(0,0,0,0.12);
    box-shadow: 0 14px 45px rgba(0,0,0,0.35);
    margin-bottom: 10px;
  }
</style>
""", unsafe_allow_html=True)

# ============================================================
# PICKS DATA (clean placeholders — replace later with real feed)
# ============================================================
PICKS = [
    {"sport":"NBA", "icon":"🏀", "game":"76ers @ Celtics", "market":"Spread", "pick":"BOS -9.5", "odds":"-110", "book":"FD",
     "confidence":78,
     "why":["Usage consolidates toward BOS creators","Bench mismatch drives margin","Pace supports separation"],
     "risk":["Late lineup flip","Blowout minutes risk","Market steam moves number"],
     "execution":"Take -9.5 to -10 max. Pass if -11+."},

    {"sport":"NBA", "icon":"🏀", "game":"Kings @ Lakers", "market":"Player 3PT Made", "pick":"Luka O 3.5 3PM", "odds":"-115", "book":"DK",
     "confidence":72,
     "why":["3PA volume is consistent","Opponent perimeter leakage","Early minutes stable"],
     "risk":["Runaway reduces 4Q volume","Cold shooting variance"],
     "execution":"Take -115 to -125. Pass at -140+."},

    {"sport":"NBA", "icon":"🏀", "game":"Knicks @ Spurs", "market":"Player Blocks", "pick":"Wemby O 4.5 BLK", "odds":"+105", "book":"MGM",
     "confidence":66,
     "why":["Opponent rim attempts","Block profile matchup","Paint touch volume"],
     "risk":["Foul trouble","Opponent goes 5-out"],
     "execution":"Prefer plus money. If it goes -130, pass."},

    {"sport":"NHL", "icon":"🏒", "game":"Knights @ Penguins", "market":"Player Shots", "pick":"Eichel O 2.5 SOG", "odds":"-120", "book":"DK",
     "confidence":80,
     "why":["Shot attempt rate","O-zone time projection","Matchup advantage"],
     "risk":["Early lead slows pace","Goalie variance"],
     "execution":"Take -120 to -135. Pass if -150+."},

    {"sport":"NHL", "icon":"🏒", "game":"Panthers @ Islanders", "market":"Player Point", "pick":"Barkov 1+ Point", "odds":"-135", "book":"FD",
     "confidence":74,
     "why":["PP exposure","Top line minutes","Possession edge"],
     "risk":["Low-event game","Goalie steal"],
     "execution":"Take -135 to -150. Avoid -170+."},

    {"sport":"MMA / UFC", "icon":"🥊", "game":"UFC Main Event", "market":"Rounds", "pick":"Over 1.5 Rounds", "odds":"-140", "book":"MGM",
     "confidence":70,
     "why":["Clinch/grappling time projection","Early finish paths suppressed","Pace projects longer"],
     "risk":["One-shot KO variance","Ref standups change control"],
     "execution":"Take -140 to -155. Pass at -180+."},

    {"sport":"MMA / UFC", "icon":"🥊", "game":"UFC Co-Main Event", "market":"Method of Victory", "pick":"Underdog by Decision", "odds":"+220", "book":"FD",
     "confidence":61,
     "why":["Cardio edge late","Control time path exists","Scorecard-friendly style"],
     "risk":["Judges variability","Early knockdown flips"],
     "execution":"Small size only. High variance prop."},
]

# ============================================================
# STATE
# ============================================================
if "selected" not in st.session_state:
    st.session_state.selected = None
if "chat" not in st.session_state:
    st.session_state.chat = []

def score(p):
    return p.get("confidence", 0)

def top3():
    return sorted(PICKS, key=lambda x: score(x), reverse=True)[:3]

def forced_one_per_game():
    by_game = {}
    for p in PICKS:
        g = p["game"]
        if g not in by_game or score(p) > score(by_game[g]):
            by_game[g] = p
    return [by_game[g] for g in sorted(by_game.keys())]

def set_selected(p):
    st.session_state.selected = p
    st.session_state.chat = []

def scotty_answer(p, q):
    why = "\n".join([f"- {x}" for x in p["why"]])
    risk = "\n".join([f"- {x}" for x in p["risk"]])

    return f"""
**Active Pick**
- Game: **{p['game']}**
- Market: **{p['market']}**
- Pick: **{p['pick']} {p['odds']}** (Book: {p['book']})
- Confidence: **{p['confidence']}%**

**Why**
{why}

**Risk**
{risk}

**Execution**
- {p['execution']}

**Your question**
{q}

**Answer (operator logic)**
- Convert your question into **probability vs price vs timing**.
- If probability changes → adjust sizing.
- If price changes → only bet inside execution limits.
- If timing changes → act early or pass. No chasing.
""".strip()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### EDGEINTEL")
    st.caption("Send the URL. No signup required.")
    if DEMO_PASS:
        st.info("Passcode gate is ON (DEMO_PASS set).")
    else:
        st.success("Open link (no passcode).")

    st.divider()
    st.caption("Click any pick on the left → it loads on the right.")

# ============================================================
# TOPBAR
# ============================================================
stamp = datetime.now().strftime("%b %d, %Y • %I:%M %p")
st.markdown(f"""
<div class="topbar">
  <div class="title">Account <span class="pill" style="margin-left:8px;">Simulated Data</span></div>
  <div class="subtitle">Top 3 Picks • Full Slate • Dossier • AI Q&A • Updated {stamp}</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# LAYOUT
# ============================================================
left, right = st.columns([1.22, 1.0], gap="large")

with left:
    st.markdown("#### 🔥 Top 3 Picks of the Day")
    for idx, p in enumerate(top3(), start=1):
        rowA, rowB = st.columns([0.78, 0.22])
        with rowA:
            st.markdown(f"""
            <div class="rowItem">
              <div class="rowLeft">
                <div class="ico">{p['icon']}</div>
                <div>
                  <div class="rowTitle">#{idx} • {p['game']}</div>
                  <div class="rowMeta">
                    {p['sport']} • {p['market']} • <span class="teal">{p['pick']} {p['odds']}</span> • {p['book']} • {p['confidence']}%
                  </div>
                </div>
              </div>
              <div><span class="badge">TOP</span></div>
            </div>
            """, unsafe_allow_html=True)
        with rowB:
            if st.button("Open", key=f"top_open_{idx}"):
                set_selected(p)

    st.markdown("#### 📋 Full Slate (One Pick per Game)")
    for p in forced_one_per_game():
        rowA, rowB = st.columns([0.78, 0.22])
        with rowA:
            st.markdown(f"""
            <div class="rowItem">
              <div class="rowLeft">
                <div class="ico">{p['icon']}</div>
                <div>
                  <div class="rowTitle">{p['game']}</div>
                  <div class="rowMeta">
                    {p['sport']} • {p['market']} • <span class="teal">{p['pick']} {p['odds']}</span> • {p['book']} • {p['confidence']}%
                  </div>
                </div>
              </div>
              <div><span class="pill">FREE</span></div>
            </div>
            """, unsafe_allow_html=True)
        with rowB:
            if st.button("Open", key=f"slate_open_{p['sport']}_{p['game']}_{p['market']}"):
                set_selected(p)

with right:
    st.markdown('<div class="detail">', unsafe_allow_html=True)
    if not st.session_state.selected:
        st.markdown("### Pick Dossier")
        st.info("Click **Open** on any pick (left). This panel will load full analysis + AI Q&A.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        p = st.session_state.selected

        st.markdown(f"""
        <div class="card">
          <div style="font-weight:950; font-size:14px;">🧠 Pick Dossier</div>
          <div class="muted" style="margin-top:6px;">
            <span class="badge">{p['sport']}</span>
            &nbsp; {p['game']}
          </div>
          <div style="margin-top:10px;">
            <b>FOR WHAT:</b> {p['market']}<br/>
            <b>PICK:</b> <span class="teal">{p['pick']} {p['odds']}</span> &nbsp; (Book: {p['book']})<br/>
            <b>CONFIDENCE:</b> {p['confidence']}%
          </div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Deep Analysis", "Ask Scotty"])

        with tab1:
            st.markdown("**Why**")
            st.markdown("\n".join([f"- {x}" for x in p["why"]]))

            st.markdown("**Risk**")
            st.markdown("\n".join([f"- {x}" for x in p["risk"]]))

            st.markdown("**Execution Rule**")
            st.write(p["execution"])

        with tab2:
            c1, c2, c3 = st.columns(3)
            if c1.button("Explain edge"):
                q = "Explain the edge in 3 bullets and what matters most."
                st.session_state.chat.append(("user", q))
                st.session_state.chat.append(("assistant", scotty_answer(p, q)))
            if c2.button("What kills it?"):
                q = "What kills this bet and how do we defend?"
                st.session_state.chat.append(("user", q))
                st.session_state.chat.append(("assistant", scotty_answer(p, q)))
            if c3.button("Sizing + timing"):
                q = "Give sizing + timing rules and when we pass."
                st.session_state.chat.append(("user", q))
                st.session_state.chat.append(("assistant", scotty_answer(p, q)))

            user_msg = st.chat_input("Ask Scotty about this pick… (scenarios, hedges, timing, price limits)")
            if user_msg:
                st.session_state.chat.append(("user", user_msg))
                st.session_state.chat.append(("assistant", scotty_answer(p, user_msg)))

            for role, content in st.session_state.chat[-12:]:
                with st.chat_message("user" if role == "user" else "assistant"):
                    st.markdown(content)

        st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.caption("Note: picks shown use simulated inputs until live odds/news feeds are connected.")
