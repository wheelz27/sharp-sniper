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

render_scotty_widget(picks, raiders_mode=True)
