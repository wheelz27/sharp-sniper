import streamlit as st
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(page_title="EDGEINTEL | Control Panel", layout="wide")

# ============================================================
# THEME (dark SaaS / like your screenshot)
# ============================================================
st.markdown("""
<style>
  .stApp { background-color: #0b1220 !important; color: #E6E8EE !important; }
  header{ visibility:hidden; }

  section[data-testid="stSidebar"]{
    background: #0a101b !important;
    border-right: 1px solid rgba(255,255,255,0.06);
  }

  /* Dark buttons */
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

  .cat {
    margin-top: 14px;
    padding-top: 10px;
    border-top: 1px solid rgba(255,255,255,0.06);
  }
  .catname {
    font-size: 11px;
    letter-spacing: 1.8px;
    font-weight: 950;
    opacity: 0.7;
    text-transform: uppercase;
    margin-bottom: 8px;
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
  .rowLeft { display:flex; align-items:center; gap: 10px; min-width: 280px; }
  .ico {
    width: 30px; height: 30px;
    border-radius: 9px;
    display:flex; align-items:center; justify-content:center;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.04);
    font-weight: 950;
  }
  .rowTitle { font-weight: 900; }
  .rowMeta { font-size: 12px; opacity: 0.75; margin-top: 2px; }
  .rowRight { display:flex; align-items:center; gap: 10px; }
  .muted { opacity: 0.72; }

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

  .teal { color: #00F5D4; font-weight: 950; }
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
</style>
""", unsafe_allow_html=True)

# ============================================================
# DEMO DATA (replace later with your real model output)
# Every pick now includes "FOR WHAT?" context: market, odds, book.
# ============================================================
DEMO_PICKS = [
    # NBA
    {"sport":"NBA", "game":"76ers @ Celtics", "market":"Spread", "pick":"BOS -9.5", "odds":"-110", "book":"FD",
     "confidence":78,
     "why":["Usage shifts toward BOS secondary scorers","Bench mismatch","Pace supports margin"],
     "risk":["Late lineup reversal","Blowout minutes risk","Market steam moves number"],
     "execution":"Take -9.5 to -10 max. Pass if -11+."},

    {"sport":"NBA", "game":"Kings @ Lakers", "market":"Player 3PT Made", "pick":"Luka O 3.5 3PM", "odds":"-115", "book":"DK",
     "confidence":72,
     "why":["High 3PA volume","Opponent perimeter leak","Early rotation minutes stable"],
     "risk":["Runaway reduces 4Q attempts","Cold shooting variance"],
     "execution":"Take -115 to -125. Pass at -140+."},

    {"sport":"NBA", "game":"Knicks @ Spurs", "market":"Player Blocks", "pick":"Wemby O 4.5 BLK", "odds":"+105", "book":"MGM",
     "confidence":66,
     "why":["Opponent rim attempts","Block profile matchup","Paint touch volume"],
     "risk":["Foul trouble","Opponent goes 5-out"],
     "execution":"Prefer plus money. If it goes -130, pass."},

    # NHL
    {"sport":"NHL", "game":"Knights @ Penguins", "market":"Player Shots", "pick":"Eichel O 2.5 SOG", "odds":"-120", "book":"DK",
     "confidence":80,
     "why":["Shot attempt rate","O-zone time projection","Matchup line advantage"],
     "risk":["Early lead slows pace","Goalie variance"],
     "execution":"Take -120 to -135. If -150, pass."},

    {"sport":"NHL", "game":"Panthers @ Islanders", "market":"Player Point", "pick":"Barkov 1+ Point", "odds":"-135", "book":"FD",
     "confidence":74,
     "why":["PP exposure","Top line minutes","Possession edge"],
     "risk":["Low-event game","Goalie steal"],
     "execution":"Take -135 to -150. Avoid -170+."},

    {"sport":"NHL", "game":"Flames @ Ducks", "market":"Player Point", "pick":"McTavish O 0.5 PTS", "odds":"-110", "book":"MGM",
     "confidence":67,
     "why":["Home form trend","Chance creation volume","Matchup usage"],
     "risk":["Randomness in points props"],
     "execution":"Take -110 to -125. Pass at -140+."},

    # UFC
    {"sport":"MMA / UFC", "game":"Fighter A vs Fighter B", "market":"Rounds", "pick":"Over 1.5 Rounds", "odds":"-140", "book":"MGM",
     "confidence":70,
     "why":["Clinch time projection","Takedown threat suppresses early KO","Finish-rate suppression"],
     "risk":["One-shot KO variance","Ref standups"],
     "execution":"Take -140 to -155. Pass at -180+."},

    {"sport":"MMA / UFC", "game":"Fighter C vs Fighter D", "market":"Method of Victory", "pick":"D by Decision", "odds":"+220", "book":"FD",
     "confidence":61,
     "why":["Cardio edge late","Control time projection","Damage differential trend"],
     "risk":["Judges variability","Early knockdown flips outcome"],
     "execution":"Small size only. Great price, high variance."},

    {"sport":"MMA / UFC", "game":"Fighter E vs Fighter F", "market":"Method of Victory", "pick":"E by KO/TKO", "odds":"+155", "book":"DK",
     "confidence":63,
     "why":["Power differential","Defense leakage","Distance control"],
     "risk":["Wrestling surprise path","Cardio dump"],
     "execution":"Small size. Only if +140 or better."},
]

# Catalog modules (the screenshot vibe)
MODULES = [
    {"cat":"BASKETBALL", "name":"NBA", "icon":"🏀", "plan":"FREE"},
    {"cat":"BASKETBALL", "name":"NCAAB", "icon":"🏀", "plan":"FREE"},
    {"cat":"FOOTBALL", "name":"NFL", "icon":"🏈", "plan":"FREE"},
    {"cat":"SOCCER", "name":"MLS", "icon":"⚽", "plan":"FREE"},
    {"cat":"TENNIS", "name":"ATP", "icon":"🎾", "plan":"FREE"},
    {"cat":"OTHER SPORTS", "name":"NHL", "icon":"🏒", "plan":"FREE"},
    {"cat":"OTHER SPORTS", "name":"MMA / UFC", "icon":"🥊", "plan":"FREE"},
]

# ============================================================
# STATE
# ============================================================
if "page" not in st.session_state:
    st.session_state.page = "Account"
if "selected_module" not in st.session_state:
    st.session_state.selected_module = None
if "selected_game" not in st.session_state:
    st.session_state.selected_game = None
if "chat" not in st.session_state:
    st.session_state.chat = []

def score(p):
    # demo ranking metric: confidence primarily
    return p.get("confidence", 0)

def picks_for_sport(sport_name):
    return [p for p in DEMO_PICKS if p["sport"] == sport_name]

def best_bet_of_day():
    return max(DEMO_PICKS, key=score)

def forced_picks_one_per_game():
    # One pick per game (already one per game in this demo list)
    # If you later have multiple markets per game, pick highest confidence per game.
    by_game = {}
    for p in DEMO_PICKS:
        g = p["game"]
        if g not in by_game or score(p) > score(by_game[g]):
            by_game[g] = p
    return [by_game[g] for g in sorted(by_game.keys())]

def set_module(m):
    st.session_state.selected_module = m
    st.session_state.selected_game = None
    st.session_state.chat = []

def set_game(pick):
    st.session_state.selected_game = pick
    st.session_state.chat = []

def scotty_answer(p, q):
    # Deterministic “deep analysis” response (stable).
    why = "\n".join([f"- {x}" for x in p["why"]])
    risk = "\n".join([f"- {x}" for x in p["risk"]])
    return f"""
**Active Pick**
- Game: **{p['game']}**
- Market: **{p['market']}**
- Pick: **{p['pick']} {p['odds']}** (Book: {p['book']})
- Confidence: **{p['confidence']}%**

**Why we picked it**
{why}

**Risk / Variance**
{risk}

**Execution Rule**
- {p['execution']}

**Your question**
{q}

**Answer**
- Translate the question into: does it change **probability**, **price**, or **timing**?
- If it changes probability → adjust confidence/sizing.
- If it changes price → only take if it’s still inside the execution rule.
- If it changes timing → act early or pass. No chasing.
""".strip()

# ============================================================
# SIDEBAR NAV
# ============================================================
with st.sidebar:
    st.markdown("### EDGEINTEL")
    st.caption("Control Panel")

    nav = st.radio("Navigation", ["Account", "Webhooks", "Docs", "Log Out"],
                   index=["Account","Webhooks","Docs","Log Out"].index(st.session_state.page),
                   label_visibility="collapsed")
    st.session_state.page = nav
    st.divider()
    st.caption("Click a module → then pick a game.")

# ============================================================
# TOPBAR
# ============================================================
stamp = datetime.now().strftime("%b %d, %Y • %I:%M %p")
st.markdown(f"""
<div class="topbar">
  <div class="title">Account</div>
  <div class="subtitle">Modules • Picks • Dossier • AI Q&A • Updated {stamp}</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# MAIN LAYOUT
# ============================================================
left, right = st.columns([1.18, 1.0], gap="large")

# ----------------------------
# LEFT: Module Catalog + Best Bet + Forced Picks
# ----------------------------
with left:
    # BEST BET OF THE DAY
    bb = best_bet_of_day()
    st.markdown(f"""
    <div class="card">
      <div style="font-weight:950; font-size:14px;">🔥 Best Bet of the Day (DEMO Ranked)</div>
      <div class="muted" style="margin-top:6px;">
        <span class="badge">{bb['sport']}</span>
        &nbsp; {bb['game']}
      </div>
      <div style="margin-top:8px;">
        <b>Market:</b> {bb['market']} &nbsp; | &nbsp;
        <b>Pick:</b> <span class="teal">{bb['pick']} {bb['odds']}</span> &nbsp; | &nbsp;
        <b>Book:</b> {bb['book']} &nbsp; | &nbsp;
        <b>Conf:</b> {bb['confidence']}%
      </div>
      <div class="muted" style="margin-top:8px;">Rule: {bb['execution']}</div>
    </div>
    """, unsafe_allow_html=True)

    # FORCED PICKS (one per game)
    st.markdown("#### Forced Picks (One per game)")
    fp = forced_picks_one_per_game()
    for p in fp:
        st.markdown(f"""
        <div class="rowItem">
          <div class="rowLeft">
            <div class="ico">🎯</div>
            <div>
              <div class="rowTitle">{p['game']}</div>
              <div class="rowMeta">
                {p['sport']} • {p['market']} • <span class="teal">{p['pick']} {p['odds']}</span> • {p['book']} • {p['confidence']}%
              </div>
            </div>
          </div>
          <div class="rowRight"><span class="pill">DEMO</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### Modules")
    q = st.text_input("Search modules", placeholder="nba, nhl, ufc...")
    cats = ["ALL"] + sorted(list({m["cat"] for m in MODULES}))
    cat = st.selectbox("Category", cats, index=0)

    filtered = MODULES
    if cat != "ALL":
        filtered = [m for m in filtered if m["cat"] == cat]
    if q.strip():
        filtered = [m for m in filtered if q.lower() in m["name"].lower()]

    grouped = {}
    for m in filtered:
        grouped.setdefault(m["cat"], []).append(m)

    for catname, items in grouped.items():
        st.markdown(f'<div class="cat"><div class="catname">{catname}</div></div>', unsafe_allow_html=True)
        for m in items:
            rowA, rowB = st.columns([0.76, 0.24])
            with rowA:
                st.markdown(f"""
                <div class="rowItem">
                  <div class="rowLeft">
                    <div class="ico">{m['icon']}</div>
                    <div>
                      <div class="rowTitle">{m['name']}</div>
                      <div class="rowMeta">Picks • Dossier • AI Q&A</div>
                    </div>
                  </div>
                  <div class="rowRight">
                    <span class="pill">{m['plan']}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
            with rowB:
                if st.button("Open", key=f"open_{m['cat']}_{m['name']}"):
                    set_module(m)
                st.button("Upgrade", key=f"up_{m['cat']}_{m['name']}")

# ----------------------------
# RIGHT: Sport Slate → Game Dossier → AI Chat
# ----------------------------
with right:
    st.markdown('<div class="detail">', unsafe_allow_html=True)

    if not st.session_state.selected_module:
        st.markdown("### Module Detail")
        st.info("Click **Open** on a module to load the slate + dossier + AI chat here.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        mod = st.session_state.selected_module
        st.markdown(f"### {mod['icon']} {mod['name']}")
        st.caption(f"{mod['cat']} • Plan: {mod['plan']}")

        sport_picks = picks_for_sport(mod["name"])

        # If module has no demo picks, show placeholder
        if not sport_picks:
            st.warning("No demo picks loaded for this module yet. Wire your model output here.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            # Slate list
            st.markdown("#### Slate (click a game)")
            for i, p in enumerate(sport_picks):
                if st.button(f"{p['game']}  •  {p['market']}  •  {p['pick']} {p['odds']}  •  {p['book']}  •  {p['confidence']}%",
                             key=f"game_{mod['name']}_{i}"):
                    set_game(p)

            st.markdown("---")

            # Dossier + AI
            if not st.session_state.selected_game:
                st.info("Select a game above to open the dossier + ask Scotty questions.")
            else:
                p = st.session_state.selected_game

                st.markdown(f"""
                <div class="card">
                  <div style="font-weight:950; font-size:14px;">🧠 Dossier</div>
                  <div class="muted" style="margin-top:6px;">
                    <span class="badge">{p['sport']}</span>
                    &nbsp; {p['game']}
                  </div>
                  <div style="margin-top:8px;">
                    <b>FOR WHAT:</b> {p['market']}<br/>
                    <b>PICK:</b> <span class="teal">{p['pick']} {p['odds']}</span> &nbsp; (Book: {p['book']})<br/>
                    <b>CONFIDENCE:</b> {p['confidence']}%
                  </div>
                </div>
                """, unsafe_allow_html=True)

                t1, t2 = st.tabs(["Deep Analysis", "Ask Scotty"])

                with t1:
                    st.markdown("**Why we picked it**")
                    st.markdown("\n".join([f"- {x}" for x in p["why"]]))

                    st.markdown("**Risk / Variance**")
                    st.markdown("\n".join([f"- {x}" for x in p["risk"]]))

                    st.markdown("**Execution Rule**")
                    st.write(p["execution"])

                with t2:
                    c1, c2, c3 = st.columns(3)
                    if c1.button("Explain the edge"):
                        q = "Explain the edge cleanly. What is the one driver that matters most?"
                        st.session_state.chat.append(("user", q))
                        st.session_state.chat.append(("assistant", scotty_answer(p, q)))
                    if c2.button("What kills it?"):
                        q = "What kills this bet and how do we defend?"
                        st.session_state.chat.append(("user", q))
                        st.session_state.chat.append(("assistant", scotty_answer(p, q)))
                    if c3.button("Sizing rules"):
                        q = "Give sizing + timing rules and when we pass."
                        st.session_state.chat.append(("user", q))
                        st.session_state.chat.append(("assistant", scotty_answer(p, q)))

                    user_msg = st.chat_input("Ask about this pick… (props, spread, scenarios, hedges, timing)")
                    if user_msg:
                        st.session_state.chat.append(("user", user_msg))
                        st.session_state.chat.append(("assistant", scotty_answer(p, user_msg)))

                    for role, content in st.session_state.chat[-12:]:
                        with st.chat_message("user" if role == "user" else "assistant"):
                            st.markdown(content)

        st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.link_button("🚀 UNLOCK FULL SYNDICATE ACCESS", "https://whop.com/YOUR_LINK", use_container_width=True)
