import streamlit as st
import pandas as pd
import random
from datetime import datetime, timezone
import time

st.set_page_config(page_title="EDGEINTEL | COMMAND CENTER", layout="wide")

# -----------------------------
# CINEMATIC CSS (glow, motion, typography, panels)
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
  width:10px; height:10px;
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

/* AI Analyst */
.ai-card{
  border-radius: 22px;
  padding: 16px;
  background: linear-gradient(135deg, rgba(88,166,255,0.12), rgba(13,17,23,0.60));
  border: 1px solid rgba(88,166,255,0.22);
}
.ai-head{
  display:flex; align-items:center; justify-content:space-between; gap:10px;
}
.ai-name{
  font-size: 14px;
  font-weight: 900;
  letter-spacing:.4px;
}
.ai-status{
  font-size: 12px;
  opacity: .85;
}
.ai-text{
  margin-top: 10px;
  font-size: 14px;
  line-height: 1.6;
  opacity: .92;
}
.mini{ font-size: 12px; opacity:.78; }

/* Typewriter (JS inject) container */
#typebox{
  white-space: pre-wrap;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono","Courier New", monospace;
  font-size: 13px;
  line-height: 1.55;
  color: #c9d1d9;
}

/* Responsive */
@media (max-width: 1100px){
  .kpi-grid{ grid-template-columns: repeat(2,1fr); }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DATA
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
            {"Game": "LAL @ BOS", "Market":"Spread", "Vegas": -5.5, "Model": -8.2, "EdgePts": 2.7, "Conf": 0.88, "Vol":"High"},
            {"Game": "NYK @ PHI", "Market":"Spread", "Vegas": +2.0, "Model": -1.5, "EdgePts": 3.5, "Conf": 0.92, "Vol":"High"},
            {"Game": "PHX @ DAL", "Market":"Spread", "Vegas": -1.0, "Model": -0.5, "EdgePts": 0.5, "Conf": 0.74, "Vol":"Med"},
            {"Game": "GSW @ DEN", "Market":"Spread", "Vegas": +4.5, "Model": +6.0, "EdgePts": 1.5, "Conf": 0.81, "Vol":"Med"},
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

    # Rank score (single “executive” number)
    # score = edge * confidence * volatility weight
    vol_w = df["Vol"].map({"High":1.08,"Med":1.00,"Low":0.96}).fillna(1.0)
    df["Score"] = (df["EdgePts"] * df["Conf"] * 100 * vol_w).round(1)

    return df.sort_values("Score", ascending=False).reset_index(drop=True)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("### Executive Controls")
    exec_mode = st.toggle("EXEC DEMO MODE (always impressive)", value=True)
    voice_on = st.toggle("🔊 AI Voice (talking briefings)", value=True)
    min_edge = st.slider("Min Edge (pts)", 0.0, 5.0, 1.5, 0.5)
    min_conf = st.slider("Min Confidence (%)", 50, 99, 85, 1)
    st.divider()
    st.markdown("### Delivery Layer")
    st.caption("Discord is optional. This is a modular alert stack.")
    st.write("✅ Web (dashboard)")
    st.write("✅ Voice (on-screen)")
    st.write("➜ Email/SMS/Push next")

df = build_edges(exec_mode)

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
# FILTER + EDGE BOARD
# -----------------------------
filtered = df[(df["EdgePts"] >= min_edge) & (df["ConfPct"] >= min_conf)].copy()

st.markdown('<div class="section-title">📊 Edge Board (Ranked Intelligence)</div>', unsafe_allow_html=True)
st.markdown('<div class="panel">', unsafe_allow_html=True)

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
# PICK DOSSIER + AI ANALYST (TALKING)
# -----------------------------
st.write("")
left, right = st.columns([1.25, 1])

if len(filtered) == 0:
    with left:
        st.warning("No edges match your filters. Lower thresholds or enable EXEC DEMO MODE.")
else:
    pick = st.selectbox("Select a pick to open the dossier", filtered["Game"].tolist())
    row = filtered[filtered["Game"] == pick].iloc[0]

    # Analyst narrative (tight, operator style)
    direction = "Model leans AWAY" if float(row["Model"]) > float(row["Vegas"]) else "Model leans HOME"
    edge_strength = "SNIPER-GRADE" if row["Tier"] == "SNIPER" else ("PRIMARY" if row["Tier"] == "PRIMARY" else "SECONDARY")
    risk_note = random.choice([
        "Risk: volatility high — execute early or skip late movement.",
        "Risk: injury confirmation may compress edge — monitor feed.",
        "Risk: public money can swing — wait for retrace if line spikes.",
        "Risk: edge is timing-sensitive — do not chase.",
    ])
    exec_guide = random.choice([
        "Execution: take it only if edge stays ≥ threshold at entry.",
        "Execution: scale small, increase only if line holds value.",
        "Execution: avoid late chase — value evaporates fast.",
        "Execution: if market corrects, downgrade tier immediately.",
    ])

    briefing = (
        f"Analyst briefing. {pick}. "
        f"Vegas is {float(row['Vegas']):+.1f}. Model fair value is {float(row['Model']):+.1f}. "
        f"Edge is plus {float(row['EdgePts']):.1f} points with confidence {int(row['ConfPct'])} percent. "
        f"Tier is {row['Tier']}. {direction}. "
        f"Reason: {row['WhyTag']}. "
        f"{risk_note} {exec_guide}"
    )

    # Dossier panel
    with left:
        st.markdown('<div class="section-title">🧾 Pick Dossier</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="panel">
          <div style="font-size:12px; opacity:0.78;">{row['Tier']} • SCORE {row['Score']} • {row['ModelVer']} • Data {row['Freshness']}</div>
          <div style="font-size:22px; font-weight:900; margin-top:6px;">{pick}</div>
          <div style="margin-top:10px; line-height:1.7;">
            <b>Vegas:</b> {float(row['Vegas']):+.1f} • <b>Model:</b> {float(row['Model']):+.1f} • <b>Edge:</b> +{float(row['EdgePts']):.1f} pts<br/>
            <b>Confidence:</b> {int(row['ConfPct'])}% • <b>Volatility:</b> {row['Vol']} • <b>Lean:</b> {direction}<br/>
            <b>Driver:</b> {row['WhyTag']}<br/>
          </div>
          <div style="margin-top:10px; font-size:12px; opacity:0.82;">
            {risk_note}<br/>
            {exec_guide}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Small “memo” block for copy/paste
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

    # AI Analyst panel with voice + typewriter
    with right:
        st.markdown('<div class="section-title">🤖 AI Analyst — Live Brief</div>', unsafe_allow_html=True)

        # Typewriter via injected JS (keeps it cinematic)
        typewriter_html = f"""
        <div class="ai-card">
          <div class="ai-head">
            <div class="ai-name">SYNDICATE ANALYST</div>
            <div class="ai-status">STATUS: LIVE • MODE: EXEC BRIEF</div>
          </div>
          <div class="mini">Press briefing to speak. (Voice uses your browser — no Discord needed.)</div>
          <div style="margin-top:10px;" id="typebox"></div>
        </div>

        <script>
          const text = `{briefing.replace("`","'")}`;
          const box = document.getElementById("typebox");
          box.innerText = "";
          let i = 0;
          function type() {{
            if (i < text.length) {{
              box.innerText += text.charAt(i);
              i++;
              setTimeout(type, 12);
            }}
          }}
          type();

          function speakNow() {{
            if (!('speechSynthesis' in window)) {{
              alert("Speech synthesis not supported in this browser.");
              return;
            }}
            window.speechSynthesis.cancel();
            const u = new SpeechSynthesisUtterance(text);
            u.rate = 1.03;
            u.pitch = 0.95;
            u.volume = 1.0;
            window.speechSynthesis.speak(u);
          }}
          window.__EDGEINTEL_SPEAK__ = speakNow;
        </script>
        """
        st.components.v1.html(typewriter_html, height=290)

        # Buttons (Streamlit → calls the JS function)
        cA, cB = st.columns(2)
        with cA:
            if st.button("🔊 AI Briefing (Speak)", use_container_width=True, disabled=not voice_on):
                st.components.v1.html("<script>window.__EDGEINTEL_SPEAK__ && window.__EDGEINTEL_SPEAK__();</script>", height=0)

        with cB:
            st.button("🛰️ Alert Test (Simulated)", use_container_width=True)

        # Tiny “threat-level” feel with a simple chart
        st.write("")
        st.markdown('<div class="section-title">📈 Signal Strength</div>', unsafe_allow_html=True)
        x = list(range(10))
        base = row["ConfPct"]
        y = [max(50, min(99, base + random.randint(-6, 6))) for _ in x]
        fig = plt.figure()
        plt.plot(x, y)
        plt.title("Confidence Trend (Last 10 ticks)")
        plt.xlabel("tick")
        plt.ylabel("confidence")
        st.pyplot(fig, clear_figure=True)

# -----------------------------
# AUDIT LOG (credibility anchor)
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
st.caption("NOTE: Voice briefing runs locally in the browser. No Discord required for the demo.")
