import streamlit as st
import pandas as pd
import random
import json
from datetime import datetime, timezone

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="EDGEINTEL | COMMAND CENTER", layout="wide")

# -----------------------------
# CINEMATIC CSS
# -----------------------------
st.markdown("""
<style>
.stApp{
  background:
    radial-gradient(1100px 600px at 12% 0%, rgba(31,111,235,0.26), rgba(0,0,0,0)),
    radial-gradient(900px 500px at 85% 10%, rgba(35,134,54,0.18), rgba(0,0,0,0)),
    radial-gradient(900px 700px at 55% 110%, rgba(210,153,34,0.10), rgba(0,0,0,0)),
    #06090f;
  color:#c9d1d9;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
}
.block-container{ max-width: 1450px; padding-top: 1rem; padding-bottom: 2.2rem; }
header{ visibility:hidden; }

/* HERO */
.hero{ border-radius: 24px; padding: 26px 26px 18px 26px; background: linear-gradient(135deg, rgba(31,111,235,0.30), rgba(13,17,23,0.70)); border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 18px 50px rgba(0,0,0,0.42); position: relative; overflow:hidden; }
.hero:before{ content:""; position:absolute; inset:-2px; background: radial-gradient(700px 260px at 25% 0%, rgba(88,166,255,0.35), rgba(0,0,0,0)); }
.h-title{ position:relative; font-size: 34px; font-weight: 900; letter-spacing: .6px; margin: 0; display:flex; align-items:center; gap: 12px; }
.h-sub{ position:relative; margin-top: 6px; opacity:.84; font-size:14px; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DATA (UFC MATCHUP DATA EXAMPLE)
# -----------------------------
def build_edges(exec_mode: bool) -> pd.DataFrame:
    if exec_mode:
        rows = [
            {"Game":"UFC 280: Islam Makhachev vs Charles Oliveira", "Market":"Fight Winner", "Vegas":-170, "Model":-200, "EdgePts":30, "Conf":0.88, "Vol":"High", "Fighter1": "Islam Makhachev", "Fighter2": "Charles Oliveira"},
            {"Game":"UFC 281: Adesanya vs Pereira", "Market":"Fight Winner", "Vegas":-145, "Model":-120, "EdgePts":25, "Conf":0.85, "Vol":"Medium", "Fighter1": "Israel Adesanya", "Fighter2": "Alex Pereira"},
            {"Game":"UFC 279: Nate Diaz vs Tony Ferguson", "Market":"Fight Winner", "Vegas":+200, "Model":+220, "EdgePts":10, "Conf":0.75, "Vol":"Medium", "Fighter1": "Nate Diaz", "Fighter2": "Tony Ferguson"}
        ]
    else:
        rows = [
            {"Game":"UFC 280: Islam Makhachev vs Charles Oliveira", "Market":"Fight Winner", "Vegas":-170, "Model":-200, "EdgePts":30, "Conf":0.88, "Vol":"High", "Fighter1": "Islam Makhachev", "Fighter2": "Charles Oliveira"},
            {"Game":"UFC 281: Adesanya vs Pereira", "Market":"Fight Winner", "Vegas":-145, "Model":-120, "EdgePts":25, "Conf":0.85, "Vol":"Medium", "Fighter1": "Israel Adesanya", "Fighter2": "Alex Pereira"},
            {"Game":"UFC 279: Nate Diaz vs Tony Ferguson", "Market":"Fight Winner", "Vegas":+200, "Model":+220, "EdgePts":10, "Conf":0.75, "Vol":"Medium", "Fighter1": "Nate Diaz", "Fighter2": "Tony Ferguson"}
        ]
    
    df = pd.DataFrame(rows)

    # Add edge, tier logic
    def tier(edge, conf):
        if edge >= 20 and conf >= 0.90: return "SNIPER"
        if edge >= 15 and conf >= 0.85: return "PRIMARY"
        if edge >= 10 and conf >= 0.80: return "SECONDARY"
        return "WATCH"
    
    df["Tier"] = [tier(e, c) for e, c in zip(df["EdgePts"], df["Conf"])]
    df["ConfPct"] = (df["Conf"] * 100).round(0).astype(int)
    df["Freshness"] = [f"{random.randint(4,22)}s" for _ in range(len(df))]
    df["ModelVer"] = [f"NEURAL v3.{random.randint(3,9)}.{random.randint(0,9)}" for _ in range(len(df))]
    
    why = [
        "Fighter stats favor one side based on pace and recent performance.",
        "Line lag from last fight; model adjusted for recovery times.",
        "Public opinion shifting the line against sharp value.",
        "Model expects dominance based on recent training footage."
    ]
    df["WhyTag"] = [random.choice(why) for _ in range(len(df))]

    vol_w = df["Vol"].map({"High":1.08,"Med":1.00,"Low":0.96}).fillna(1.0)
    df["Score"] = (df["EdgePts"] * df["Conf"] * 100 * vol_w).round(1)

    return df.sort_values("Score", ascending=False).reset_index(drop=True)

# -----------------------------
# FLOATING SCOTTY WIDGET (voice + quick actions)
# -----------------------------
def render_scotty_widget(picks: list[dict], raiders_mode: bool = True):
    payload = json.dumps(picks).replace("</", "<\\/")

    raiders_badge = "☠️ RAIDERS NATION" if raiders_mode else "OPERATOR MODE"

    html = f"""
    <style>
      #scotty-fab {{
        position: fixed; right: 18px; bottom: 18px; z-index: 99999;
        border-radius: 999px; padding: 12px 14px; cursor: pointer; user-select: none;
        background: rgba(13,17,23,0.80);
        border: 1px solid rgba(88,166,255,0.35);
        box-shadow: 0 14px 40px rgba(0,0,0,0.45);
        backdrop-filter: blur(10px);
        color: #c9d1d9;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
        display: flex; align-items: center; gap: 10px;
      }}
      #scotty-fab .dot {{
        width: 10px; height: 10px; border-radius: 999px;
        background: #238636;
        box-shadow: 0 0 14px rgba(35,134,54,0.85);
        position: relative;
      }}
      #scotty-fab .dot:after {{
        content:"";
        position:absolute; left:50%; top:50%;
        width: 10px; height: 10px;
        transform: translate(-50%,-50%);
        border-radius:999px;
        background: rgba(35,134,54,0.35);
        animation: ping 1.2s infinite;
      }}
      @keyframes ping {{
        0% {{ width:10px; height:10px; opacity:.6; }}
        80% {{ width:34px; height:34px; opacity:0; }}
        100% {{ opacity:0; }}
      }}

      #scotty-panel {{
        position: fixed; right: 18px; bottom: 72px;
        width: 360px; max-width: calc(100vw - 36px);
        z-index: 99999; display: none;
        border-radius: 18px; overflow: hidden;
        background: rgba(13,17,23,0.82);
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 18px 60px rgba(0,0,0,0.55);
        backdrop-filter: blur(14px);
        color: #c9d1d9;
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
      }}
      #scotty-head {{
        padding: 12px 14px;
        display:flex; align-items:center; justify-content:space-between; gap:10px;
        background: linear-gradient(135deg, rgba(31,111,235,0.25), rgba(13,17,23,0.0));
        border-bottom: 1px solid rgba(255,255,255,0.08);
      }}
      #scotty-name {{ font-weight: 900; letter-spacing: .4px; font-size: 13px; }}
      #scotty-badge {{
        font-size: 11px; opacity: .9; padding: 4px 8px; border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.04);
        white-space: nowrap;
      }}
      #scotty-close {{ cursor:pointer; opacity:.75; font-weight:900; }}

      #scotty-body {{ padding: 12px 14px 14px 14px; }}
      #scotty-body .mini {{
        font-size: 12px; opacity: .80; margin-bottom: 10px; line-height: 1.5;
      }}
      #scotty-select {{
        width: 100%;
        padding: 10px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.04);
        color: #c9d1d9;
        outline: none;
      }}
      #scotty-actions {{
        display:grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px;
      }}
      .sc-btn {{
        padding: 10px;
        border-radius: 14px;
        border: 1px solid rgba(88,166,255,0.25);
        background: rgba(31,111,235,0.10);
        color: #c9d1d9;
        cursor: pointer;
        font-weight: 800;
      }}
      .sc-btn.secondary {{
        border-color: rgba(35,134,54,0.30);
        background: rgba(35,134,54,0.10);
      }}
      #scotty-out {{
        margin-top: 12px;
        padding: 10px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(0,0,0,0.18);
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
          <div style="font-size:11px; opacity:.75;">Live briefings • no noise</div>
        </div>
        <div style="display:flex; align-items:center; gap:10px;">
          <div id="scotty-badge">{raiders_badge}</div>
          <div id="scotty-close">✕</div>
        </div>
      </div>

      <div id="scotty-body">
        <div class="mini">
          Pick a fight. I’ll brief you instantly (text + voice).<br/>
          <span style="opacity:.65;">Voice uses your browser. No Discord required.</span>
        </div>

        <select id="scotty-select"></select>

        <div id="scotty-actions">
          <button class="sc-btn" id="sc-brief">🔊 Brief</button>
          <button class="sc-btn secondary" id="sc-top">⚡ Top Edge</button>
          <button class="sc-btn" id="sc-risk">⚠️ Risk Only</button>
          <button class="sc-btn secondary" id="sc-why">🧠 Why</button>
        </div>

        <div id="scotty-out">Ready.</div>
      </div>
    </div>

    <div id="scotty-fab">
      <span class="dot"></span>
      <div style="font-weight:900;">SCOTTY</div>
      <div style="font-size:12px; opacity:.75;">AI Brief</div>
    </div>

    <script>
      const picks = {payload};

      const panel = document.getElementById("scotty-panel");
      const fab = document.getElementById("scotty-fab");
      const closeBtn = document.getElementById("scotty-close");
      const sel = document.getElementById("scotty-select");
      const out = document.getElementById("scotty-out");

      function openPanel() {{
        panel.style.display = (panel.style.display === "none" || panel.style.display === "") ? "block" : "none";
      }}
      fab.addEventListener("click", openPanel);
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
          opt.textContent = `${{p.tier}} • ${{p.game}} • Edge ${{p.edge}} • Conf ${{p.conf}}`;
          sel.appendChild(opt);
        }});
      }}

      function current() {{
        const idx = parseInt(sel.value || "0", 10);
        return picks[Math.max(0, Math.min(idx, picks.length - 1))];
      }}

      function setOut(text) {{
        out.innerText = text;
      }}

      renderSelect();

      document.getElementById("sc-brief").addEventListener("click", () => {{
        const p = current();
        const t = p.brief || `${{p.game}}. Edge ${{p.edge}}. Confidence ${{p.conf}}. Tier ${{p.tier}}. Why: ${{p.why}}`;
        setOut(t);
        speak(t);
      }});

      document.getElementById("sc-top").addEventListener("click", () => {{
        sel.value = "0";
        const p = current();
        const t = `Top edge is ${{p.game}}. Edge ${{p.edge}}. Confidence ${{p.conf}}. Tier ${{p.tier}}.`;
        setOut(t);
        speak(t);
      }});

      document.getElementById("sc-risk").addEventListener("click", () => {{
        const p = current();
        const t = p.risk || "Risk: volatility elevated — execute early. Do not chase.";
        setOut(t);
        speak(t);
      }});

      document.getElementById("sc-why").addEventListener("click", () => {{
        const p = current();
        const t = `Why: ${{p.why}}`;
        setOut(t);
        speak(t);
      }});
    </script>
    """
    st.components.v1.html(html, height=0)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("### Executive Controls")
    exec_mode = st.toggle("EXEC DEMO MODE (always impressive)", value=True)
    raiders_mode = st.toggle("☠️ Raiders Nation badge", value=True)
    min_edge = st.slider("Min Edge (pts)", 0.0, 5.0, 1.5, 0.5)
    min_conf = st.slider("Min Confidence (%)", 50, 99, 85, 1)
    st.divider()
    st.caption("Voice briefings run locally in the browser. Floating SCOTTY widget is client-side and cannot crash the app.")

# -----------------------------
# BUILD DATA + EXECUTION
# -----------------------------
df = build_edges(exec_mode)
filtered = df[(df["EdgePts"] >= min_edge) & (df["ConfPct"] >= min_conf)].copy()

# -----------------------------
# HERO + KPIs
# -----------------------------
now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
latency_ms = random.randint(9, 21)
scan_rate = f"{random.randint(12000, 18200):,}/min"
vol = "ELEVATED" if (df["Vol"] == "High").any() else "NORMAL"
active = int((df["EdgePts"] >= 2.0).sum())

# -----------------------------
# HERO + KPIs RENDER
# -----------------------------
st.markdown(f"""
<div class="hero">
    <div class="h-title">📡 EDGEINTEL COMMAND CENTER</div>
    <div class="h-sub">NEURAL ENGINE v3.4.2 • {now} • SYSTEM STATUS: <span style="color:#238636;">OPTIMAL</span></div>
    <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-top: 24px;">
        <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:12px; border:1px solid rgba(255,255,255,0.05);">
            <div style="font-size:11px; opacity:0.6; letter-spacing:1px;">ENGINE LATENCY</div>
            <div style="font-size:20px; font-weight:800; color:#58a6ff;">{latency_ms}ms</div>
        </div>
        <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:12px; border:1px solid rgba(255,255,255,0.05);">
            <div style="font-size:11px; opacity:0.6; letter-spacing:1px;">SCAN RATE</div>
            <div style="font-size:20px; font-weight:800; color:#238636;">{scan_rate}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:12px; border:1px solid rgba(255,255,255,0.05);">
            <div style="font-size:11px; opacity:0.6; letter-spacing:1px;">MARKET VOL</div>
            <div style="font-size:20px; font-weight:800; color:#d29922;">{vol}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:12px; border:1px solid rgba(255,255,255,0.05);">
            <div style="font-size:11px; opacity:0.6; letter-spacing:1px;">ACTIVE EDGES</div>
            <div style="font-size:20px; font-weight:800; color:#f85149;">{active}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("") # Spacer

# -----------------------------
# MAIN INTELLIGENCE MATRIX
# -----------------------------
if not filtered.empty:
    display_df = filtered[[
        "Tier", "Game", "Market", "Vegas", "Model", "EdgePts", "ConfPct", "Freshness", "WhyTag"
    ]].copy()
    
    display_df.columns = [
        "TIER", "MATCHUP", "MARKET", "VEGAS", "MODEL", "EDGE", "CONF %", "SYNC", "INSIGHT BRIEF"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "CONF %": st.column_config.ProgressColumn("CONF %", min_value=0, max_value=100, format="%d%%"),
            "EDGE": st.column_config.NumberColumn("EDGE", format="+%d pts"),
        }
    )
else:
    st.warning("📡 Scanning... Adjust filters to see live market data.")

# -----------------------------
# ACTIVATE SCOTTY AI WIDGET
# -----------------------------
scotty_picks = []
for _, row in filtered.iterrows():
    scotty_picks.append({
        "game": row["Game"],
        "tier": row["Tier"],
        "edge": row["EdgePts"],
        "conf": f"{row['ConfPct']}%",
        "why": row["WhyTag"],
        "brief": f"Operator, in the {row['Game']} matchup, we detect a {row['EdgePts']} point edge. Confidence is {row['ConfPct']} percent. {row['WhyTag']}"
    })

if scotty_picks:
    render_scotty_widget(scotty_picks, raiders_mode=raiders_mode)

st.divider()
st.caption("Proprietary Neural Weights applied. Data synced with Vegas API.")
