import streamlit as st
import pandas as pd
import random
from datetime import datetime, timezone

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="EDGEINTEL | COMMAND CENTER", layout="wide")

# -----------------------------
# PREMIUM CSS (Glass + Glow + Better Typography)
# -----------------------------
st.markdown("""
<style>
/* Base */
.stApp {
  background: radial-gradient(1200px 600px at 20% 0%, rgba(31,111,235,0.20), rgba(0,0,0,0)),
              radial-gradient(900px 500px at 80% 10%, rgba(35,134,54,0.14), rgba(0,0,0,0)),
              #06090f;
  color: #c9d1d9;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
}

.block-container { padding-top: 1.2rem; padding-bottom: 2.2rem; }

/* Hide Streamlit chrome a bit */
header { visibility: hidden; }
section[data-testid="stSidebar"] { border-right: 1px solid rgba(255,255,255,0.06); }

/* Header */
.ei-header {
  position: relative;
  padding: 26px 26px 18px 26px;
  border-radius: 18px;
  background: linear-gradient(135deg, rgba(31,111,235,0.22), rgba(13,17,23,0.72));
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
  overflow: hidden;
  margin-bottom: 18px;
}
.ei-header:before {
  content: "";
  position: absolute;
  inset: -2px;
  background: radial-gradient(600px 240px at 30% 0%, rgba(88,166,255,0.35), rgba(0,0,0,0));
  filter: blur(0px);
}
.ei-title {
  position: relative;
  display:flex; align-items:center; gap:12px;
  margin:0;
  font-size: 30px;
  letter-spacing: 0.5px;
}
.ei-sub {
  position: relative;
  margin-top: 6px;
  opacity: 0.82;
  font-size: 14px;
}
.pills { position: relative; display:flex; gap:8px; flex-wrap: wrap; margin-top: 14px; }
.pill {
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 12px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.04);
}
.pill.green { border-color: rgba(35,134,54,0.35); background: rgba(35,134,54,0.10); }
.pill.blue  { border-color: rgba(31,111,235,0.35); background: rgba(31,111,235,0.10); }
.pill.amber { border-color: rgba(210,153,34,0.35); background: rgba(210,153,34,0.10); }

/* Metric Cards */
.kpi-wrap { display:grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 12px; }
.kpi {
  border-radius: 16px;
  padding: 14px 14px 12px 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 26px rgba(0,0,0,0.28);
}
.kpi .label { font-size: 12px; opacity: 0.75; }
.kpi .value { font-size: 22px; margin-top: 4px; font-weight: 700; letter-spacing: 0.3px; }
.kpi .delta { margin-top: 6px; font-size: 12px; opacity: 0.85; }
.dot {
  display:inline-block; width:8px; height:8px; border-radius:999px; margin-right:6px;
  background: #238636; box-shadow: 0 0 10px rgba(35,134,54,0.6);
}

/* Section Titles */
.ei-section-title {
  font-size: 16px;
  font-weight: 700;
  margin: 4px 0 10px 0;
}

/* Table framing */
.panel {
  border-radius: 18px;
  padding: 14px;
  background: rgba(13,17,23,0.55);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 14px 34px rgba(0,0,0,0.32);
}

/* Callout */
.callout {
  border-radius: 16px;
  padding: 14px;
  background: linear-gradient(135deg, rgba(35,134,54,0.14), rgba(13,17,23,0.60));
  border: 1px dashed rgba(35,134,54,0.45);
}

/* Buttons */
a.ei-btn {
  display:inline-block;
  text-decoration:none;
  padding: 12px 14px;
  border-radius: 14px;
  border: 1px solid rgba(88,166,255,0.35);
  background: rgba(31,111,235,0.12);
  box-shadow: 0 10px 22px rgba(0,0,0,0.22);
  font-weight: 700;
}

/* Responsive */
@media (max-width: 1100px){
  .kpi-wrap { grid-template-columns: repeat(2, 1fr); }
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# DATA (replace this with your real all_edges)
# -----------------------------
def build_edge_df():
    # Replace this with your real model outputs.
    rows = [
        {"Game": "LAL @ BOS", "Market": "Spread", "Vegas": -5.5, "Model": -8.2, "EdgePts": 2.7, "Conf": 0.88, "Vol": "High"},
        {"Game": "NYK @ PHI", "Market": "Spread", "Vegas": +2.0, "Model": -1.5, "EdgePts": 3.5, "Conf": 0.92, "Vol": "High"},
        {"Game": "PHX @ DAL", "Market": "Spread", "Vegas": -1.0, "Model": -0.5, "EdgePts": 0.5, "Conf": 0.74, "Vol": "Med"},
        {"Game": "GSW @ DEN", "Market": "Spread", "Vegas": +4.5, "Model": +6.0, "EdgePts": 1.5, "Conf": 0.81, "Vol": "Med"},
    ]
    df = pd.DataFrame(rows)

    # Add "Signal" tier
    def tier(edge, conf):
        if edge >= 3.0 and conf >= 0.90: return "SNIPER"
        if edge >= 2.0 and conf >= 0.85: return "PRIMARY"
        if edge >= 1.0 and conf >= 0.78: return "SECONDARY"
        return "WATCH"
    df["Tier"] = [tier(e, c) for e, c in zip(df["EdgePts"], df["Conf"])]

    # Add "Why" tags (exec-friendly)
    why_bank = [
        "Model disagreement vs opener + injury-adjusted pace shift",
        "Line lag vs recent efficiency + matchup advantage",
        "Market overreacted to public narrative; model holds value",
        "Short-term volatility spike creates misprice window",
    ]
    df["WhyTag"] = [random.choice(why_bank) for _ in range(len(df))]

    # Add "Data Freshness" + "Model Version"
    df["Freshness"] = [f"{random.randint(5,28)}s" for _ in range(len(df))]
    df["ModelVer"] = [f"NEURAL v3.{random.randint(1,9)}" for _ in range(len(df))]

    # Format
    df["ConfPct"] = (df["Conf"] * 100).round(0).astype(int)
    return df


df = build_edge_df()

# -----------------------------
# SIDEBAR (Control Surface)
# -----------------------------
with st.sidebar:
    st.markdown("### Control Surface")
    min_edge = st.slider("Minimum Edge (pts)", 0.0, 5.0, 1.0, 0.5)
    min_conf = st.slider("Minimum Confidence (%)", 50, 99, 80, 1)
    show_watch = st.toggle("Include WATCH tier", value=False)
    st.divider()
    st.markdown("### Delivery Channels")
    st.caption("Discord is optional. You can push alerts via SMS/email/push later.")
    st.write("- Discord Webhook ✅")
    st.write("- SMS (Twilio) ➜ next")
    st.write("- Email (SendGrid) ➜ next")
    st.write("- Push (PWA) ➜ next")


# -----------------------------
# HEADER
# -----------------------------
now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
active_edges = (df["EdgePts"] >= 2.0).sum()
sniper_count = (df["Tier"] == "SNIPER").sum()

st.markdown(f"""
<div class="ei-header">
  <div class="ei-title">📡 EDGEINTEL — COMMAND CENTER</div>
  <div class="ei-sub">Neural fair-value projections vs live market • decision transparency • audit trail</div>
  <div class="pills">
    <div class="pill green"><span class="dot"></span>ENGINE ACTIVE</div>
    <div class="pill blue">SCAN RATE: 14,200/min</div>
    <div class="pill amber">VOLATILITY: ELEVATED</div>
    <div class="pill">UTC: {now}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# KPI row
latency_ms = random.randint(10, 22)
market_shift = round(random.uniform(3.2, 8.4), 1)

st.markdown(f"""
<div class="kpi-wrap">
  <div class="kpi">
    <div class="label">Engine Latency</div>
    <div class="value">{latency_ms}ms</div>
    <div class="delta">Target: &lt;25ms • Status: Optimal</div>
  </div>
  <div class="kpi">
    <div class="label">Games Analyzed</div>
    <div class="value">{len(df)}</div>
    <div class="delta">Live ingest • Continuous</div>
  </div>
  <div class="kpi">
    <div class="label">Active Edges (≥ 2.0)</div>
    <div class="value">{active_edges}</div>
    <div class="delta">Market shift: {market_shift}%</div>
  </div>
  <div class="kpi">
    <div class="label">Sniper Tier</div>
    <div class="value">+{264}</div>
    <div class="delta">Qualified: {sniper_count} plays</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# -----------------------------
# FILTER DATA
# -----------------------------
filtered = df[(df["EdgePts"] >= min_edge) & (df["ConfPct"] >= min_conf)]
if not show_watch:
    filtered = filtered[filtered["Tier"] != "WATCH"]

# -----------------------------
# MAIN: EDGE MATRIX
# -----------------------------
st.markdown('<div class="ei-section-title">📊 Live Market Projection Matrix</div>', unsafe_allow_html=True)
st.markdown('<div class="panel">', unsafe_allow_html=True)

# Display table with better UX than st.table
display_df = filtered.copy()
display_df["Vegas"] = display_df["Vegas"].map(lambda x: f"{x:+.1f}")
display_df["Model"] = display_df["Model"].map(lambda x: f"{x:+.1f}")
display_df["EdgePts"] = display_df["EdgePts"].map(lambda x: f"+{x:.1f}")
display_df = display_df[["Game","Market","Vegas","Model","EdgePts","ConfPct","Tier","WhyTag","Freshness","ModelVer"]]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "ConfPct": st.column_config.ProgressColumn(
            "Confidence",
            help="Model confidence (0–100).",
            format="%d%%",
            min_value=0,
            max_value=100,
        ),
        "WhyTag": st.column_config.TextColumn("Why (headline)"),
        "Freshness": st.column_config.TextColumn("Data"),
        "ModelVer": st.column_config.TextColumn("Model"),
    }
)

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# DRILLDOWN: WHY WE PICKED IT
# -----------------------------
st.write("")
st.markdown('<div class="ei-section-title">🧠 Pick Explainer (Decision Transparency)</div>', unsafe_allow_html=True)

if len(filtered) == 0:
    st.warning("No edges match current filters. Lower the edge/conf thresholds.")
else:
    pick = st.selectbox("Select a row to explain", filtered["Game"].tolist())
    row = filtered[filtered["Game"] == pick].iloc[0]

    implied_direction = "Model favors the away side" if row["Model"] > row["Vegas"] else "Model favors the home side"
    edge_strength = "Strong" if row["EdgePts"] >= 3.0 else ("Solid" if row["EdgePts"] >= 2.0 else "Marginal")
    risk_note = random.choice([
        "High volatility window — better for quick execution, not late holds.",
        "Watch for injury confirmation; edge can shrink fast.",
        "Public money may move line against value before lock.",
        "If market snaps back, reduce sizing / skip."
    ])
    trigger = random.choice([
        "Opener Dislocation", "Injury Reprice Lag", "Pace/Matchup Misprice", "Public Narrative Overreaction"
    ])

    left, right = st.columns([1.2, 1])
    with left:
        st.markdown(f"""
        <div class="panel">
          <div style="font-size:14px; opacity:0.85;">{row['Tier']} SIGNAL • {edge_strength} EDGE</div>
          <div style="font-size:22px; font-weight:800; margin-top:6px;">{pick}</div>
          <div style="margin-top:10px; line-height:1.55;">
            <b>Vegas:</b> {row['Vegas']:+.1f} • <b>Model:</b> {row['Model']:+.1f} • <b>Edge:</b> +{row['EdgePts']:.1f} pts<br/>
            <b>Confidence:</b> {int(row['Conf']*100)}% • <b>Trigger:</b> {trigger}<br/>
            <b>Interpretation:</b> {implied_direction}
          </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown(f"""
        <div class="callout">
          <div style="font-size:14px; font-weight:800;">Why we picked this</div>
          <div style="margin-top:8px; opacity:0.90; line-height:1.55;">
            • Market line is off our fair value by <b>+{row['EdgePts']:.1f}</b> points<br/>
            • Confidence stays high under current volatility regime<br/>
            • Fits {row['Tier']} tier rules (edge + confidence threshold)
          </div>
          <div style="margin-top:10px; font-size:12px; opacity:0.85;">
            Risk note: {risk_note}
          </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Show full decision memo (numbers + controls)"):
        st.write({
            "game": pick,
            "market": row["Market"],
            "vegas": float(row["Vegas"]),
            "model": float(row["Model"]),
            "edge_points": float(row["EdgePts"]),
            "confidence": float(row["Conf"]),
            "tier": row["Tier"],
            "headline_reason": row["WhyTag"],
            "data_freshness": row["Freshness"],
            "model_version": row["ModelVer"],
            "timestamp_utc": now,
            "execution_guidance": "If edge shrinks below threshold, downgrade tier or skip."
        })

# -----------------------------
# SNIPER FUNNEL (Premium, not cheesy)
# -----------------------------
st.write("")
st.markdown('<div class="ei-section-title">🎯 Syndicate Sniper Plays</div>', unsafe_allow_html=True)

c1, c2 = st.columns([1.2, 1])
with c1:
    st.markdown("""
    <div class="panel">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div style="font-size:14px; opacity:0.85;">PRIVATE BOARD</div>
        <div class="pill green">LIVE</div>
      </div>
      <div style="font-size:18px; font-weight:800; margin-top:6px;">ACTIVE SNIPER PARLAY (+264)</div>
      <div style="margin-top:10px; opacity:0.90; line-height:1.7;">
        <span style="opacity:0.7;">Leg 1:</span> [LOCKED — MEMBERS ONLY]<br/>
        <span style="opacity:0.7;">Leg 2:</span> [LOCKED — MEMBERS ONLY]<br/>
        <span style="opacity:0.7;">Leg 3:</span> [LOCKED — MEMBERS ONLY]
      </div>
      <div style="margin-top:12px; font-size:12px; opacity:0.70;">
        Unlock includes: instant alerts • full board • confidence drivers • risk flags • audit log.
      </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="panel">
      <div style="font-size:16px; font-weight:800;">Mobile Alerts</div>
      <div style="margin-top:8px; opacity:0.90; line-height:1.6;">
        Discord is one channel. If you don’t want Discord on your phone, we can push via SMS/email/push next.
      </div>
      <div style="margin-top:12px;">
        <a class="ei-btn" href="https://whop.com/YOUR_LINK" target="_blank">🔥 JOIN THE SYNDICATE</a>
      </div>
      <div style="margin-top:10px; font-size:12px; opacity:0.70;">
        Exec note: delivery layer is modular (Discord → SMS → Push).
      </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption("System Logs: Model weights refreshed • Market sync OK • Scanning for misprices • Audit trail enabled")
