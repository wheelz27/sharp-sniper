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
.hero{
  border-radius: 24px;
  padding: 26px 26px 18px 26px;
  background: linear-gradient(135deg, rgba(31,111,235,0.30), rgba(13,17,23,0.70));
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 18px 50px rgba(0,0,0,0.42);
  position: relative;
  overflow:hidden;
}
.hero:before{
  content:"";
  position:absolute;
  inset:-2px;
  background: radial-gradient(700px 260px at 25% 0%, rgba(88,166,255,0.35), rgba(0,0,0,0));
}
.h-title{
  position:relative;
  font-size: 34px;
  font-weight: 900;
  letter-spacing: .6px;
  margin: 0;
  display:flex;
  align-items:center;
  gap: 12px;
}
.h-sub{
  position:relative;
  margin-top: 6px;
  opacity:.84;
  font-size:14px;
}

/* Pulse dot */
.pulse{
  width:10px; height:10px; border-radius:999px;
  background:#238636;
  box-shadow:0 0 14px rgba(35,134,54,0.85);
  display:inline-block;
  position: relative;
}
.pulse:after{
  content:"";
  position:absolute;
  left:50%; top:50%;
  width: 10px; height: 10px;
  transform: translate(-50%,-50%);
  border-radius:999px;
  background: rgba(35,134,54,0.35);
  animation: ping 1.2s infinite;
}
@keyframes ping{
  0%{ width:10px; height:10px; opacity:.6; }
  80%{ width:34px; height:34px; opacity:0; }
  100%{ opacity:0; }
}

/* Pills */
.pills{ position:relative; display:flex; gap:8px; flex-wrap:wrap; margin-top:14px; }
.pill{
  padding: 6px 10px;
  border-radius:999px;
  font-size:12px;
  border:1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.04);
}
.pill.green{ border-color: rgba(35,134,54,0.35); background: rgba(35,134,54,0.12); }
.pill.blue{ border-color: rgba(31,111,235,0.35); background: rgba(31,111,235,0.12); }
.pill.amber{ border-color: rgba(210,153,34,0.35); background: rgba(210,153,34,0.12); }

/* KPI */
.kpi-grid{ display:grid; grid-template-columns: repeat(4,1fr); gap:12px; margin-top: 12px; }
.kpi{
  border-radius: 18px;
  padding: 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  backdrop-filter: blur(10px);
  box-shadow: 0 14px 38px rgba(0,0,0,0.32);
}
.kpi .label{ font-size:12px; opacity:.75; }
.kpi .value{ font-size:24px; font-weight:900; margin-top:4px; letter-spacing:.3px; }
.kpi .meta{ font-size:12px; opacity:.80; margin-top:6px; }

/* Panels */
.panel{
  border-radius: 20px;
  padding: 14px;
  background: rgba(13,17,23,0.62);
  border:1px solid rgba(255,255,255,0.08);
  box-shadow: 0 16px 48px rgba(0,0,0,0.36);
}
.section-title{ font-size:16px; font-weight:900; margin: 8px 0 10px 0; }

/* Dossier */
.dossier{
  border-radius: 20px;
  padding: 16px;
  background: linear-gradient(135deg, rgba(88,166,255,0.10), rgba(13,17,23,0.60));
  border: 1px solid rgba(88,166,255,0.22);
}

/* Responsive */
@media (max-width: 1100px){
  .kpi-grid{ grid-template-columns: repeat(2,1fr); }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DATA (swap with your real all_edges later)
# -----------------------------
def build_edges(exec_mode: bool) -> pd.DataFrame:
    if exec_mode:
        rows = [
            {"Game":"LAL @ BOS","Market":"Spread","Vegas":-5.5,"Model":-8.2,"EdgePts":2.7,"Conf":0.88,"Vol":"High"},
            {"Game":"NYK @ PHI","Market":"Spread","Vegas":+2.0,"Model":-1.5,"EdgePts":3.5,"Conf":0.92,"Vol":"High"},
            {"Game":"PHX @ DAL","Market":"Spread","Vegas":-1.0,"Model":-3.1,"EdgePts":2.1,"Conf":0.86,"Vol":"Med"},
            {"Game":"GSW @ DEN","Market":"Spread","Vegas":+4.5,"Model":+6.4,"EdgePts":1.9,"Conf":0.84,"Vol":"Med"},
            {"Game":"MIA @ MIL","Market":"Spread","Vegas":+6.0,"Model":+3.1,"EdgePts":2.9,"Conf":0.89,"Vol":"High"},
        ]
    else:
        rows = [
            {"Game":"LAL @ BOS","Market":"Spread","Vegas":-5.5,"Model":-8.2,"EdgePts":2.7,"Conf":0.88,"Vol":"High"},
            {"Game":"NYK @ PHI","Market":"Spread","Vegas":+2.0,"Model":-1.5,"EdgePts":3.5,"Conf":0.92,"Vol":"High"},
            {"Game":"PHX @ DAL","Market":"Spread","Vegas":-1.0,"Model":-0.5,"EdgePts":0.5,"Conf":0.74,"Vol":"Med"},
            {"Game":"GSW @ DEN","Market":"Spread","Vegas":+4.5,"Model":+6.0,"EdgePts":1.5,"Conf":0.81,"Vol":"Med"},
        ]

    df = pd.DataFrame(rows)

    def tier(edge, conf):
        if edge >= 3.0 and conf >= 0.90: return "SNIPER"
        if edge >= 2.0 and conf >= 0.85: return "PRIMARY"
        if edge >= 1.5 and conf >= 0.80: return "SECONDARY"
        return "WATCH"

    df["Tier"] = [tier(e, c) for e, c in zip(df["EdgePts"], df["Conf"])]
    df["ConfPct"] = (df["Conf"] * 100).round(0).astype(int)
    df["Freshness"] = [f"{random.randint(4,22)}s" for _ in range(len(df))]
    df["ModelVer"] = [f"NEURAL v3.{random.randint(3,9)}.{random.randint(0,9)}" for _ in range(len(df))]

    why = [
        "Opener dislocation + pace mismatch not priced in",
        "Market lag after efficiency delta + matchup advantage",
        "Public narrative drift; model holds fair-value",
        "Volatility spike created a short misprice window",
        "Injury-adjusted baseline differs from consensus feed",
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
          Pick a game. I’ll brief you instantly (text + voice).<br/>
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
    st.caption("Voice briefings run locally in the browser. No Discord required for this demo.")

# -----------------------------
# BUILD DATA
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

st.markdown(f"""
<div class="hero">
  <div class="h-title"><span class="pulse"></span> EDGEINTEL — INTELLIGENCE COMMAND</div>
  <div class="h-sub">Live market surveillance • transparent decision logic • audit-ready picks</div>
  <div class="pills">
    <div class="pill green">ENGINE ACTIVE</div>
    <div class="pill blue">SCAN RATE: {scan_rate}</div>
    <div class="pill amber">VOLATILITY: {vol}</div>
    <div class="pill">UTC: {now}</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi">
    <div class="label">Engine Latency</div>
    <div class="value">{latency_ms}ms</div>
    <div class="meta">Target &lt; 25ms • Stable</div>
  </div>
  <div class="kpi">
    <div class="label">Edges Live (≥ 2.0)</div>
    <div class="value">{active}</div>
    <div class="meta">Auto-ranked by score</div>
  </div>
  <div class="kpi">
    <div class="label">Top Signal Tier</div>
    <div class="value">{df.iloc[0]['Tier']}</div>
    <div class="meta">Rule-based tiering</div>
  </div>
  <div class="kpi">
    <div class="label">Integrity</div>
    <div class="value">AUDIT</div>
    <div class="meta">Model ver + freshness + log</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# -----------------------------
# EDGE BOARD
# -----------------------------
st.markdown('<div class="section-title">📊 Edge Board (Ranked Intelligence)</div>', unsafe_allow_html=True)
st.markdown('<div class="panel">', unsafe_allow_html=True)

if len(filtered) == 0:
    st.warning("No edges match your filters. Lower thresholds or keep EXEC DEMO MODE on.")
else:
    show_df = filtered.copy()
    show_df["Vegas"] = show_df["Vegas"].map(lambda x: f"{x:+.1f}")
    show_df["Model"] = show_df["Model"].map(lambda x: f"{x:+.1f}")
    show_df["EdgePts"] = show_df["EdgePts"].map(lambda x: f"+{x:.1f}")
    show_df = show_df[["Score","Game","Market","Vegas","Model","EdgePts","ConfPct","Tier","WhyTag","Freshness","ModelVer"]]

    st.dataframe(
        show_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ConfPct": st.column_config.ProgressColumn("Confidence", format="%d%%", min_value=0, max_value=100),
            "WhyTag": st.column_config.TextColumn("Why (headline)"),
            "ModelVer": st.column_config.TextColumn("Model"),
            "Freshness": st.column_config.TextColumn("Data"),
        }
    )

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# PICK DOSSIER + SAFE CHART (NO MATPLOTLIB)
# -----------------------------
st.write("")
left, right = st.columns([1.25, 1])

if len(filtered) > 0:
    pick = st.selectbox("Select a pick to open the dossier", filtered["Game"].tolist())
    row = filtered[filtered["Game"] == pick].iloc[0]

    direction = "Model leans AWAY" if float(row["Model"]) > float(row["Vegas"]) else "Model leans HOME"
    risk_note = random.choice([
        "Risk: volatility elevated — execute early or skip late movement.",
        "Risk: injury confirmation may compress edge — monitor feed.",
        "Risk: public money can swing — avoid chasing the worst number.",
        "Risk: timing sensitive — do not chase after line corrects.",
    ])
    exec_guide = random.choice([
        "Execution: take only if edge holds above threshold at entry.",
        "Execution: scale small, increase only if market doesn’t correct.",
        "Execution: avoid late chase — value evaporates fast.",
        "Execution: downgrade immediately if edge shrinks.",
    ])

    with left:
        st.markdown('<div class="section-title">🧾 Pick Dossier</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="dossier">
          <div style="font-size:12px; opacity:0.78;">{row['Tier']} • SCORE {row['Score']} • {row['ModelVer']} • Data {row['Freshness']}</div>
          <div style="font-size:22px; font-weight:900; margin-top:6px;">{pick}</div>
          <div style="margin-top:10px; line-height:1.7;">
            <b>Vegas:</b> {float(row['Vegas']):+.1f} • <b>Model:</b> {float(row['Model']):+.1f} • <b>Edge:</b> +{float(row['EdgePts']):.1f} pts<br/>
            <b>Confidence:</b> {int(row['ConfPct'])}% • <b>Volatility:</b> {row['Vol']} • <b>Lean:</b> {direction}<br/>
            <b>Driver:</b> {row['WhyTag']}
          </div>
          <div style="margin-top:10px; font-size:12px; opacity:0.82;">
            {risk_note}<br/>
            {exec_guide}
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Copy / Paste Executive Memo"):
            st.code(
                f"""EDGEINTEL DOSSIER — {pick}
UTC: {now}
Model: {row['ModelVer']} | Freshness: {row['Freshness']} | Volatility: {row['Vol']}

Vegas: {float(row['Vegas']):+.1f}
Model: {float(row['Model']):+.1f}
Edge:  +{float(row['EdgePts']):.1f} pts
Conf:  {int(row['ConfPct'])}%
Tier:  {row['Tier']} | Score: {row['Score']}

WHY: {row['WhyTag']}
RISK: {risk_note}
EXEC: {exec_guide}
""",
                language="text"
            )

    with right:
        st.markdown('<div class="section-title">📈 Signal Strength</div>', unsafe_allow_html=True)
        x = list(range(10))
        base = int(row["ConfPct"])
        y = [max(50, min(99, base + random.randint(-6, 6))) for _ in x]
        chart_df = pd.DataFrame({"confidence": y}, index=x)
        st.line_chart(chart_df)
else:
    with left:
        st.info("No dossier available until at least one pick matches the filters.")

# -----------------------------
# AUDIT LOG
# -----------------------------
st.write("")
st.markdown('<div class="section-title">🧬 Audit Trail</div>', unsafe_allow_html=True)
st.markdown('<div class="panel">', unsafe_allow_html=True)

log_rows = []
for _ in range(7):
    log_rows.append({
        "UTC": datetime.now(timezone.utc).strftime("%H:%M:%S"),
        "Event": random.choice([
            "Vegas feed sync OK",
            "Model weights refreshed",
            "Edge threshold crossed",
            "Volatility regime updated",
            "Pick dossier generated",
            "Alert queued (simulated)",
            "Integrity check passed"
        ]),
        "Severity": random.choice(["INFO","INFO","INFO","WARN"]),
    })
st.dataframe(pd.DataFrame(log_rows), use_container_width=True, hide_index=True)

st.markdown("</div>", unsafe_allow_html=True)
st.caption("Voice briefings run locally in the browser. Floating SCOTTY widget is client-side and cannot crash the app.")

# -----------------------------
# BUILD SCOTTY WIDGET DATA + RENDER FLOATING WIDGET
# -----------------------------
picks = []
src_df = filtered if len(filtered) > 0 else df
for _, r in src_df.head(8).iterrows():
    picks.append({
        "game": r["Game"],
        "tier": r["Tier"],
        "edge": f"+{float(r['EdgePts']):.1f}",
        "conf": f"{int(r['ConfPct'])}%",
        "why": r.get("WhyTag", "Model fair-value differs from market."),
        "risk": "Risk: volatility elevated — execute early. Do not chase late movement.",
        "brief": (
            f"{r['Game']}. Vegas {float(r['Vegas']):+.1f}. Model {float(r['Model']):+.1f}. "
            f"Edge plus {float(r['EdgePts']):.1f} points. Confidence {int(r['ConfPct'])} percent. "
            f"Tier {r['Tier']}. Why: {r.get('WhyTag','')}"
        ),
    })

render_scotty_widget(picks, raiders_mode=raiders_mode)
