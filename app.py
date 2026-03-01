import streamlit as st
import json
from datetime import datetime

# -----------------------------
# 1) PAGE CONFIG + THEME
# -----------------------------
st.set_page_config(page_title="EDGEINTEL | SYNDICATE", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0D1117 !important; color: #E6E8EE !important; }

    /* TOP WHALE CARD */
    .whale-card {
        background: linear-gradient(135deg, #161B22 0%, #2E1A47 100%);
        border: 1px solid #30363D; border-left: 5px solid #00F5D4;
        border-radius: 14px; padding: 24px; margin-bottom: 22px;
        box-shadow: 0 18px 60px rgba(0,0,0,0.35);
    }

    /* SPORT HEADER */
    .sport-header {
        font-size: 0.9rem; font-weight: 900; color: #00F5D4;
        letter-spacing: 2px; text-transform: uppercase;
        border-bottom: 1px solid #30363D; padding-bottom: 8px; margin: 26px 0 14px 0;
    }

    /* GAME CARD */
    .game-card {
        background: linear-gradient(180deg, #161B22 0%, rgba(22,27,34,0.65) 100%);
        border: 1px solid #30363D;
        border-radius: 12px; padding: 18px; height: 100%;
        box-shadow: 0 12px 40px rgba(0,0,0,0.22);
    }

    .sharp-teal { color: #00F5D4; font-weight: 900; }
    .muted { color: rgba(230,232,238,0.70); }

    .prop-badge {
        display:inline-block;
        background: rgba(0, 245, 212, 0.10); color: #00F5D4;
        padding: 4px 10px; border-radius: 7px; font-size: 0.8rem; font-weight: 800;
        border: 1px solid rgba(0, 245, 212, 0.28);
    }

    .pill {
        display:inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 800;
        border: 1px solid rgba(255,255,255,0.12);
        background: rgba(255,255,255,0.04);
        margin-right: 8px;
    }

    .panel {
        background: #0f1520;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 16px;
    }

    .neural-box {
        background: #161B22;
        border-left: 4px solid #00F5D4;
        padding: 18px;
        border-radius: 12px;
        margin-top: 12px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.22);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 2) DATA (DEMO BOARD)
# -----------------------------
# IMPORTANT: This is demo/simulated intel until you wire a real feed.
master_data = {
    "NBA": [
        {"game": "76ers @ Celtics", "spread": "BOS -9.5", "prop": "J. Brown O 27.5 PTS",
         "intel": "DEMO INTEL: injury/news simulation. Edge driven by usage shift + bench mismatch.",
         "why": "Usage + pace + matchup advantage in wing scoring.",
         "risk": "Risk: late line correction. Don’t chase the worst number."},
        {"game": "Knicks @ Spurs", "spread": "SAS -1.5", "prop": "Wemby O 4.5 BLK",
         "intel": "DEMO INTEL: volatility spot — defense vs rim pressure trend.",
         "why": "Rim attempts + block rate model triggers.",
         "risk": "Risk: foul trouble swings prop outcomes."},
        {"game": "Kings @ Lakers", "spread": "LAL -13.0", "prop": "Luka O 3.5 3PM",
         "intel": "DEMO INTEL: blowout risk but usage stays high early.",
         "why": "Shot quality + opponent perimeter leakage.",
         "risk": "Risk: reduced minutes if runaway."}
    ],
    "TENNIS": [
        {"game": "MGM Slam: Kyrgios vs Bublik", "spread": "KYR ML", "prop": "O 12.5 Aces",
         "intel": "DEMO INTEL: fast indoor profile boosts serve dominance.",
         "why": "Surface speed + serve hold projection.",
         "risk": "Risk: motivation variance."},
        {"game": "IW: Golubic vs Stakusic", "spread": "GOL -3.5", "prop": "U 20.5 Games",
         "intel": "DEMO INTEL: grinder conditions; breaks cluster.",
         "why": "Return points + longer rallies compress totals.",
         "risk": "Risk: tiebreak flips under."},
        {"game": "MGM Slam: Fritz vs Paul", "spread": "FRITZ -115", "prop": "Fritz 1st Set ML",
         "intel": "DEMO INTEL: first-set aggression edge.",
         "why": "Opening set hold + first strike advantage.",
         "risk": "Risk: slow start variance."}
    ],
    "NHL": [
        {"game": "Panthers @ Islanders", "spread": "FLA -145", "prop": "Barkov 1+ Point",
         "intel": "DEMO INTEL: rest edge + possession profile.",
         "why": "Top line matchup + PP exposure.",
         "risk": "Risk: goalie variance."},
        {"game": "Knights @ Penguins", "spread": "VGK ML", "prop": "Eichel O 2.5 Shots",
         "intel": "DEMO INTEL: volume shoots up in favorable matchups.",
         "why": "Shot attempts rate + zone time projection.",
         "risk": "Risk: early lead can slow pace."},
        {"game": "Flames @ Ducks", "spread": "ANA -1.5", "prop": "McTavish O 0.5 PTS",
         "intel": "DEMO INTEL: young core heating up at home.",
         "why": "Line matching + recent xGF trend.",
         "risk": "Risk: empty net variance for puckline."}
    ],
    "MLS": [
        {"game": "Orlando @ Miami", "spread": "MIA -115", "prop": "Messi O 1.5 SOT",
         "intel": "DEMO INTEL: derby intensity + shot volume spike.",
         "why": "SOT model sees high-volume role.",
         "risk": "Risk: early goal changes shot profile."},
        {"game": "San Diego FC @ St. Louis", "spread": "SDFC -190", "prop": "Lozano Assist",
         "intel": "DEMO INTEL: chance creation dominance.",
         "why": "Key pass + xA trigger.",
         "risk": "Risk: finishing variance."},
        {"game": "Austin @ DC United", "spread": "AUS -110", "prop": "O 2.5 Goals",
         "intel": "DEMO INTEL: high press opens transitions.",
         "why": "Both teams create high-xG sequences.",
         "risk": "Risk: early red card breaks totals."}
    ],
    "UFC": [
        {"game": "UFC: Fighter A vs Fighter B", "spread": "A -150", "prop": "Over 1.5 Rounds",
         "intel": "DEMO INTEL: grappling neutralizes early KO paths; tempo projects longer.",
         "why": "Finish-rate suppression + clinch time projection.",
         "risk": "Risk: one-shot KO variance."},
        {"game": "UFC: Fighter C vs Fighter D", "spread": "D +135", "prop": "D by Decision",
         "intel": "DEMO INTEL: cardio edge + late round scoring bias.",
         "why": "Round 3 volume and control time projection.",
         "risk": "Risk: judges variability."},
        {"game": "UFC: Fighter E vs Fighter F", "spread": "E -110", "prop": "E by KO/TKO",
         "intel": "DEMO INTEL: chin mismatch + power differential.",
         "why": "Power shots landed + defense leakage model.",
         "risk": "Risk: wrestling surprise path."}
    ],
}

# -----------------------------
# 3) SESSION STATE
# -----------------------------
if "active_sport" not in st.session_state:
    st.session_state.active_sport = None
if "active_game" not in st.session_state:
    st.session_state.active_game = None
if "active_payload" not in st.session_state:
    st.session_state.active_payload = None

if "chat" not in st.session_state:
    st.session_state.chat = []  # list of {"role": "user"/"assistant", "content": str}

def set_intel(sport, g):
    st.session_state.active_sport = sport
    st.session_state.active_game = g["game"]
    st.session_state.active_payload = g

# -----------------------------
# 4) SIDEBAR (EXEC CONTROL)
# -----------------------------
with st.sidebar:
    st.markdown("### Executive Controls")
    demo_badge = st.toggle("Demo / Simulated Intel Mode", value=True)
    raiders_mode = st.toggle("☠️ Raiders Nation (Scotty)", value=True)
    st.divider()
    st.caption("This is presentation-grade. Wire a live feed later without changing the UI.")

# -----------------------------
# 5) TOP HEADER + KPI PILLS
# -----------------------------
st.title("🏛️ EDGEINTEL SYNDICATE")
stamp = datetime.now().strftime("%b %d, %Y • %I:%M %p")
mode_label = "DEMO INTEL" if demo_badge else "LIVE MODE"
st.markdown(
    f"""
    <div class="panel">
      <span class="pill">MODE: <span class="sharp-teal">{mode_label}</span></span>
      <span class="pill">SCAN: <span class="sharp-teal">ACTIVE</span></span>
      <span class="pill">UPDATED: <span class="sharp-teal">{stamp}</span></span>
      <span class="pill">VOICE: <span class="sharp-teal">BROWSER</span></span>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 6) TOP WHALE PLAY (STATIC HERO)
# -----------------------------
st.markdown("""
<div class="whale-card">
    <div style="color: #00F5D4; font-weight: 900; font-size: 0.75rem; letter-spacing: 2px;">🚨 SUNDAY MAX UNIT</div>
    <h2 style="margin: 10px 0;">FEATURED WHALE PLAY (DEMO)</h2>
    <p style="font-size: 1.05rem; margin: 0;">
      <b>SPREAD: <span class="sharp-teal">CELTICS -9.5</span></b>
      &nbsp; | &nbsp;
      <b>PROP: <span class="prop-badge">J. BROWN OVER 27.5 PTS</span></b>
      <br/><span class="muted">Narrative: usage shift + bench mismatch. Execute early, don’t chase.</span>
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# 7) GLOBAL BOARD (TOP 3 EACH SPORT)
# -----------------------------
for sport, games in master_data.items():
    st.markdown(f'<div class="sport-header">📡 TOP 3 {sport} SLATE</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, g in enumerate(games):
        with cols[i]:
            st.markdown(f"""
            <div class="game-card">
                <div style="font-weight:900; margin-bottom:8px;">{g['game']}</div>
                <div style="margin-bottom:10px;">Spread: <span class="sharp-teal">{g['spread']}</span></div>
                <div style="margin-bottom:12px;"><span class="prop-badge">🔥 {g['prop']}</span></div>
                <div class="muted" style="font-size:12px; line-height:1.45;">
                    {g['why']}
                    <br/><span style="opacity:0.8;">{g['risk']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.button("SCAN INTEL", key=f"btn_{sport}_{i}", on_click=set_intel, args=(sport, g), use_container_width=True)

# -----------------------------
# 8) SCOTTY “NEURAL LINK” (CHAT + DOSSIER)
# -----------------------------
def scotty_answer(payload, question):
    """
    Deterministic, stable “AI analyst” response.
    Swap this with a real LLM later — the UI stays the same.
    """
    game = payload["game"]
    spread = payload["spread"]
    prop = payload["prop"]
    why = payload["why"]
    risk = payload["risk"]
    intel = payload["intel"]

    raiders_line = "☠️ Raiders Nation. Scotty’s watching the board." if raiders_mode else "Operator mode engaged."

    return (
        f"{raiders_line}\n\n"
        f"**Dossier — {game}**\n"
        f"- Spread: **{spread}**\n"
        f"- Prop: **{prop}**\n"
        f"- Why: **{why}**\n"
        f"- Risk: **{risk}**\n\n"
        f"**Your question:** {question}\n\n"
        f"**Scotty’s take (demo analyst):**\n"
        f"- This question matters because it changes **probability vs price**.\n"
        f"- Base thesis: {intel}\n"
        f"- Execution rule: if the number moves against you, **don’t chase** — reduce size or skip.\n"
        f"- If you want, I’ll generate a **1-paragraph executive memo** you can paste anywhere."
    )

if st.session_state.active_game and st.session_state.active_payload:
    st.markdown("---")
    sport = st.session_state.active_sport
    payload = st.session_state.active_payload

    st.subheader(f"🧠 NEURAL LINK: {sport} • {st.session_state.active_game}")

    st.markdown(
        f"""
        <div class="neural-box">
          <b style="color:#00F5D4;">SYNDICATE SCAN:</b> {payload['intel']}<br/>
          <span class="muted">This is demo intel unless you connect a live feed.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # quick controls
    qcol1, qcol2, qcol3 = st.columns(3)
    with qcol1:
        if st.button("📌 Give me the WHY", use_container_width=True):
            st.session_state.chat.append({"role": "user", "content": "Explain why this is picked."})
            st.session_state.chat.append({"role": "assistant", "content": scotty_answer(payload, "Explain why this is picked.")})
    with qcol2:
        if st.button("⚠️ Give me the RISK", use_container_width=True):
            st.session_state.chat.append({"role": "user", "content": "What’s the main risk and how do we avoid it?"})
            st.session_state.chat.append({"role": "assistant", "content": scotty_answer(payload, "What’s the main risk and how do we avoid it?")})
    with qcol3:
        if st.button("🧾 Generate Exec Memo", use_container_width=True):
            memo_q = "Generate an executive memo for this pick."
            st.session_state.chat.append({"role": "user", "content": memo_q})
            st.session_state.chat.append({"role": "assistant", "content": scotty_answer(payload, memo_q)})

    st.markdown("")

    user_q = st.text_input(
        "Interrogate this matchup:",
        placeholder="e.g. 'What would invalidate this edge?' or 'How do we size this?'"
    )
    if user_q:
        st.session_state.chat.append({"role": "user", "content": user_q})
        st.session_state.chat.append({"role": "assistant", "content": scotty_answer(payload, user_q)})

    # render chat
    if st.session_state.chat:
        st.markdown("### Scotty Feed")
        for msg in st.session_state.chat[-10:]:
            if msg["role"] == "user":
                st.markdown(f"**You:** {msg['content']}")
            else:
                st.markdown(f"**SCOTTY:** {msg['content']}")

# -----------------------------
# 9) FLOATING SCOTTY WIDGET (VOICE + QUICK BRIEF)
# -----------------------------
# Build pick list for widget from the whole board:
widget_picks = []
for sport, games in master_data.items():
    for g in games:
        widget_picks.append({
            "sport": sport,
            "game": g["game"],
            "spread": g["spread"],
            "prop": g["prop"],
            "why": g["why"],
            "risk": g["risk"],
            "brief": f"{sport}. {g['game']}. Spread {g['spread']}. Prop {g['prop']}. Why: {g['why']}. Risk: {g['risk']}."
        })

payload_js = json.dumps(widget_picks).replace("</", "<\\/")

badge = "☠️ RAIDERS" if raiders_mode else "OPERATOR"

floating_html = f"""
<style>
  #scotty-fab {{
    position: fixed; right: 18px; bottom: 18px; z-index: 99999;
    border-radius: 999px; padding: 12px 14px; cursor: pointer; user-select: none;
    background: rgba(13,17,23,0.86);
    border: 1px solid rgba(0,245,212,0.30);
    box-shadow: 0 14px 44px rgba(0,0,0,0.48);
    backdrop-filter: blur(12px);
    color: #E6E8EE;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
    display: flex; align-items: center; gap: 10px;
  }}
  #scotty-fab .dot {{
    width: 10px; height: 10px; border-radius: 999px;
    background: #00F5D4;
    box-shadow: 0 0 18px rgba(0,245,212,0.85);
    position: relative;
  }}
  #scotty-panel {{
    position: fixed; right: 18px; bottom: 72px;
    width: 380px; max-width: calc(100vw - 36px);
    z-index: 99999; display: none;
    border-radius: 16px; overflow: hidden;
    background: rgba(13,17,23,0.88);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 20px 70px rgba(0,0,0,0.60);
    backdrop-filter: blur(16px);
    color: #E6E8EE;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
  }}
  #scotty-head {{
    padding: 12px 14px;
    display:flex; align-items:center; justify-content:space-between; gap:10px;
    background: linear-gradient(135deg, rgba(0,245,212,0.18), rgba(46,26,71,0.25));
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }}
  #scotty-name {{ font-weight: 950; letter-spacing: .5px; font-size: 12px; }}
  #scotty-badge {{
    font-size: 11px; opacity: .9; padding: 4px 8px; border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.04);
    white-space: nowrap;
  }}
  #scotty-close {{ cursor:pointer; opacity:.75; font-weight:900; }}
  #scotty-body {{ padding: 12px 14px 14px 14px; }}
  #scotty-select {{
    width: 100%;
    padding: 10px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.10);
    background: rgba(255,255,255,0.04);
    color: #E6E8EE;
    outline: none;
  }}
  #scotty-actions {{
    display:grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;
  }}
  .sc-btn {{
    padding: 10px;
    border-radius: 12px;
    border: 1px solid rgba(0,245,212,0.22);
    background: rgba(0,245,212,0.08);
    color: #E6E8EE;
    cursor: pointer;
    font-weight: 900;
  }}
  .sc-btn.secondary {{
    border-color: rgba(255,255,255,0.12);
    background: rgba(255,255,255,0.06);
  }}
  #scotty-out {{
    margin-top: 12px;
    padding: 10px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(0,0,0,0.20);
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono","Courier New", monospace;
    font-size: 12px;
    line-height: 1.55;
    white-space: pre-wrap;
  }}
</style>

<div id="scotty-panel">
  <div id="scotty-head">
    <div>
      <div id="scotty-name">SCOTTY // FLOATING ANALYST</div>
      <div style="font-size:11px; opacity:.78;">Instant briefings • voice + text</div>
    </div>
    <div style="display:flex; align-items:center; gap:10px;">
      <div id="scotty-badge">{badge}</div>
      <div id="scotty-close">✕</div>
    </div>
  </div>

  <div id="scotty-body">
    <select id="scotty-select"></select>

    <div id="scotty-actions">
      <button class="sc-btn" id="sc-brief">🔊 BRIEF</button>
      <button class="sc-btn secondary" id="sc-why">🧠 WHY</button>
      <button class="sc-btn secondary" id="sc-risk">⚠️ RISK</button>
      <button class="sc-btn" id="sc-stop">⛔ STOP</button>
    </div>

    <div id="scotty-out">Ready.</div>
  </div>
</div>

<div id="scotty-fab">
  <span class="dot"></span>
  <div style="font-weight:950;">SCOTTY</div>
  <div style="font-size:12px; opacity:.78;">AI Brief</div>
</div>

<script>
  const picks = {payload_js};

  const panel = document.getElementById("scotty-panel");
  const fab = document.getElementById("scotty-fab");
  const closeBtn = document.getElementById("scotty-close");
  const sel = document.getElementById("scotty-select");
  const out = document.getElementById("scotty-out");

  function togglePanel() {{
    panel.style.display = (panel.style.display === "none" || panel.style.display === "") ? "block" : "none";
  }}
  fab.addEventListener("click", togglePanel);
  closeBtn.addEventListener("click", () => panel.style.display = "none");

  function speak(text) {{
    if (!('speechSynthesis' in window)) {{
      out.innerText = "Voice not supported on this browser.";
      return;
    }}
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.rate = 1.02;
    u.pitch = 0.92;
    u.volume = 1.0;
    window.speechSynthesis.speak(u);
  }}

  function renderSelect() {{
    sel.innerHTML = "";
    picks.forEach((p, i) => {{
      const opt = document.createElement("option");
      opt.value = String(i);
      opt.textContent = `${{p.sport}} • ${{p.game}}`;
      sel.appendChild(opt);
    }});
  }}

  function current() {{
    const idx = parseInt(sel.value || "0", 10);
    return picks[Math.max(0, Math.min(idx, picks.length - 1))];
  }}

  renderSelect();

  document.getElementById("sc-brief").addEventListener("click", () => {{
    const p = current();
    const t = p.brief;
    out.innerText = t;
    speak(t);
  }});

  document.getElementById("sc-why").addEventListener("click", () => {{
    const p = current();
    const t = `WHY: ${{p.why}}`;
    out.innerText = t;
    speak(t);
  }});

  document.getElementById("sc-risk").addEventListener("click", () => {{
    const p = current();
    const t = `RISK: ${{p.risk}}`;
    out.innerText = t;
    speak(t);
  }});

  document.getElementById("sc-stop").addEventListener("click", () => {{
    if ('speechSynthesis' in window) window.speechSynthesis.cancel();
    out.innerText = "Stopped.";
  }});
</script>
"""

st.components.v1.html(floating_html, height=0)

# -----------------------------
# 10) PAYWALL CTA
# -----------------------------
st.divider()
st.link_button("🚀 UNLOCK FULL SYNDICATE ACCESS", "https://whop.com/YOUR_LINK", use_container_width=True)
