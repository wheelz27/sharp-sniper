import os
import time
import json
import math
import sqlite3
from datetime import datetime, timezone

import requests
import streamlit as st

# =========================
# CONFIG
# =========================
DEFAULT_SPORT = "upcoming"   # you can change in UI
REGIONS = "us,eu"
MARKETS = "h2h"
ODDS_API_BASE = "https://api.the-odds-api.com/v4"

SHARP_BOOK_KEY = "pinnacle"
MIN_EV_PCT_DEFAULT = 2.5
MAX_EV_PCT_DEFAULT = 20.0

DB_PATH = "sharpsniper.db"

# =========================
# HELPERS
# =========================
def now_utc_iso():
    return datetime.now(timezone.utc).isoformat()

def parse_commence_time(commence_time_str: str) -> datetime:
    # The Odds API returns ISO8601, usually with 'Z'
    # Example: "2026-02-28T20:00:00Z"
    s = commence_time_str.replace("Z", "+00:00")
    return datetime.fromisoformat(s)

def de_vig_probs_decimal_odds(prices: list[float]) -> list[float]:
    # Basic proportional de-vig (good enough for v1)
    implied = [1.0 / p for p in prices if p and p > 1e-9]
    total = sum(implied)
    if total <= 0:
        return []
    return [(1.0 / p) / total for p in prices]

def ev_pct(prob: float, odds: float) -> float:
    # EV = (p*(odds-1)) - (1-p)
    ev = (prob * (odds - 1.0)) - (1.0 - prob)
    return ev * 100.0

def get_api_key() -> str:
    # Prefer Streamlit secrets, fallback to env
    key = ""
    if hasattr(st, "secrets") and "THE_ODDS_API_KEY" in st.secrets:
        key = str(st.secrets["THE_ODDS_API_KEY"]).strip()
    if not key:
        key = os.getenv("THE_ODDS_API_KEY", "").strip()
    return key

def http_get_json(url: str, timeout=25):
    resp = requests.get(url, timeout=timeout)
    return resp, resp.json() if resp.content else None

# =========================
# DB
# =========================
def db_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def db_init():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS picks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_utc TEXT NOT NULL,
        sport_key TEXT NOT NULL,
        event_id TEXT NOT NULL,
        commence_utc TEXT NOT NULL,
        home_team TEXT,
        away_team TEXT,
        market TEXT NOT NULL,
        selection TEXT NOT NULL,
        book TEXT NOT NULL,
        odds REAL NOT NULL,
        sharp_book TEXT NOT NULL,
        sharp_odds_json TEXT NOT NULL,
        fair_prob REAL NOT NULL,
        ev_pct REAL NOT NULL,
        closing_odds REAL,
        clv REAL
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_picks_event ON picks(event_id);")
    conn.commit()
    conn.close()

def db_insert_pick(row: dict):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO picks (
        created_utc, sport_key, event_id, commence_utc, home_team, away_team,
        market, selection, book, odds, sharp_book, sharp_odds_json,
        fair_prob, ev_pct, closing_odds, clv
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        row["created_utc"], row["sport_key"], row["event_id"], row["commence_utc"],
        row.get("home_team"), row.get("away_team"),
        row["market"], row["selection"], row["book"], row["odds"],
        row["sharp_book"], row["sharp_odds_json"],
        row["fair_prob"], row["ev_pct"],
        row.get("closing_odds"), row.get("clv")
    ))
    conn.commit()
    conn.close()

def db_recent(limit=200):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM picks
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

def db_events_needing_closing(limit=1000):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
    SELECT id, sport_key, event_id, commence_utc, selection
    FROM picks
    WHERE closing_odds IS NULL
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

def db_set_closing(pick_id: int, closing_odds: float, clv: float):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("""
    UPDATE picks
    SET closing_odds = ?, clv = ?
    WHERE id = ?
    """, (closing_odds, clv, pick_id))
    conn.commit()
    conn.close()

# =========================
# CORE ENGINE
# =========================
def scan_edges(api_key: str, sport_key: str, min_ev: float, max_ev: float):
    url = f"{ODDS_API_BASE}/sports/{sport_key}/odds/?apiKey={api_key}&regions={REGIONS}&markets={MARKETS}"
    resp, data = http_get_json(url)
    status = resp.status_code

    diag = {
        "status": status,
        "url": url.split("apiKey=")[0] + "apiKey=***",
        "games_total": 0,
        "games_with_pinnacle": 0,
        "bookmakers_total": 0,
        "edges_total": 0,
        "reason_no_edges": ""
    }

    if status != 200 or not isinstance(data, list):
        diag["reason_no_edges"] = f"Bad response. status={status}. body={str(data)[:300]}"
        return [], diag

    diag["games_total"] = len(data)

    edges = []
    for game in data:
        event_id = game.get("id")
        commence_time = game.get("commence_time")
        home = game.get("home_team")
        away = game.get("away_team")
        books = game.get("bookmakers", []) or []
        diag["bookmakers_total"] += len(books)

        pinnacle = next((b for b in books if b.get("key") == SHARP_BOOK_KEY), None)
        if not pinnacle:
            continue
        diag["games_with_pinnacle"] += 1

        # Pinnacle outcomes
        try:
            pm = pinnacle["markets"][0]
            pout = pm["outcomes"]
        except Exception:
            continue

        sharp_prices = [o.get("price") for o in pout]
        if not all(sharp_prices):
            continue

        probs = de_vig_probs_decimal_odds([float(p) for p in sharp_prices])
        if not probs or len(probs) != len(pout):
            continue

        prob_by_name = {pout[i]["name"]: probs[i] for i in range(len(pout))}
        sharp_odds_json = json.dumps({o["name"]: o.get("price") for o in pout})

        # compare other books
        for book in books:
            if book.get("key") == SHARP_BOOK_KEY:
                continue
            book_title = book.get("title", book.get("key", "unknown"))
            try:
                bm = book["markets"][0]
                bout = bm["outcomes"]
            except Exception:
                continue

            for o in bout:
                sel = o.get("name")
                price = o.get("price")
                if not sel or not price:
                    continue
                if sel not in prob_by_name:
                    continue  # ignore mismatched naming
                p = float(prob_by_name[sel])
                odds = float(price)

                edge = ev_pct(p, odds)
                if min_ev < edge < max_ev:
                    edges.append({
                        "sport_key": sport_key,
                        "event_id": event_id,
                        "commence_utc": commence_time,
                        "home_team": home,
                        "away_team": away,
                        "market": MARKETS,
                        "selection": sel,
                        "book": book_title,
                        "odds": odds,
                        "sharp_book": SHARP_BOOK_KEY,
                        "sharp_odds_json": sharp_odds_json,
                        "fair_prob": p,
                        "ev_pct": edge
                    })

    diag["edges_total"] = len(edges)
    if diag["edges_total"] == 0:
        if diag["games_total"] == 0:
            diag["reason_no_edges"] = "No games returned for this sport_key."
        elif diag["games_with_pinnacle"] == 0:
            diag["reason_no_edges"] = "No Pinnacle lines in returned games. Try a different sport_key or regions/market."
        else:
            diag["reason_no_edges"] = "No edges passed your EV filters. Lower MIN_EV or raise MAX_EV."

    edges.sort(key=lambda x: x["ev_pct"], reverse=True)
    return edges, diag

def pick_closing_odds_for_selection(api_key: str, sport_key: str, event_id: str, selection: str):
    # We’ll use Pinnacle as “closing-ish” reference (v1).
    # This is NOT perfect “true close”, but it’s consistent and measurable.
    url = f"{ODDS_API_BASE}/sports/{sport_key}/odds/?apiKey={api_key}&regions={REGIONS}&markets={MARKETS}"
    resp, data = http_get_json(url)
    if resp.status_code != 200 or not isinstance(data, list):
        return None

    game = next((g for g in data if g.get("id") == event_id), None)
    if not game:
        return None

    books = game.get("bookmakers", []) or []
    pinnacle = next((b for b in books if b.get("key") == SHARP_BOOK_KEY), None)
    if not pinnacle:
        return None

    try:
        pout = pinnacle["markets"][0]["outcomes"]
    except Exception:
        return None

    for o in pout:
        if o.get("name") == selection:
            return float(o.get("price"))
    return None

# =========================
# UI
# =========================
st.set_page_config(page_title="Sharp Sniper (Asset Mode)", page_icon="🎯", layout="wide")
db_init()

st.title("🎯 Sharp Sniper — Asset Mode")
st.caption("We’re not building a picks app. We’re building a proprietary signal + dataset.")

api_key = get_api_key()
if not api_key:
    st.error("Missing API key. Add Streamlit Secret: THE_ODDS_API_KEY = \"...\"  (Settings → Secrets).")
    st.stop()

tabs = st.tabs(["Scanner", "History", "CLV Update"])

with tabs[0]:
    colA, colB, colC = st.columns(3)
    with colA:
        sport_key = st.text_input("sport_key", value=DEFAULT_SPORT, help="Try: upcoming, soccer_epl, basketball_nba, americanfootball_nfl, etc.")
    with colB:
        min_ev = st.number_input("MIN_EV %", value=MIN_EV_PCT_DEFAULT, step=0.5)
    with colC:
        max_ev = st.number_input("MAX_EV %", value=MAX_EV_PCT_DEFAULT, step=0.5)

    run = st.button("Run Scan", type="primary")

    if run:
        edges, diag = scan_edges(api_key, sport_key.strip(), float(min_ev), float(max_ev))

        st.subheader("Diagnostics (so we stop guessing)")
        st.write({
            "Odds API status": diag["status"],
            "games_total": diag["games_total"],
            "games_with_pinnacle": diag["games_with_pinnacle"],
            "bookmakers_seen": diag["bookmakers_total"],
            "edges_found": diag["edges_total"],
            "if_none": diag["reason_no_edges"],
        })

        if not edges:
            st.warning("No +EV picks found (per your filters). Lower MIN_EV to 1.0 or try a specific sport_key.")
            st.stop()

        top_5 = edges[:5]

        left, right = st.columns([2, 1])
        with left:
            st.subheader("🏆 Daily 5 (Ranked)")
            for i, p in enumerate(top_5, 1):
                game = f"{p.get('home_team')} vs {p.get('away_team')}"
                st.success(
                    f"**{i}. {p['selection']}**  @ **{p['odds']}**  ({p['book']})  |  **EV: {p['ev_pct']:.2f}%**\n\n"
                    f"*{game}*  |  Commence: {p.get('commence_utc')}"
                )

        with right:
            st.subheader("🔥 2 Parlays (display only)")
            if len(top_5) >= 2:
                o = top_5[0]["odds"] * top_5[1]["odds"]
                st.info(f"**Safe 2-leg:** {top_5[0]['selection']} + {top_5[1]['selection']}\n\nEst. decimal odds: **{o:.2f}**")
            if len(top_5) >= 5:
                o = top_5[2]["odds"] * top_5[3]["odds"] * top_5[4]["odds"]
                st.info(f"**Aggressive 3-leg:** {top_5[2]['selection']} + {top_5[3]['selection']} + {top_5[4]['selection']}\n\nEst. decimal odds: **{o:.2f}**")

        st.divider()
        st.subheader("Log Picks (this is how the asset is born)")

        if st.button("✅ Log Top 5 to Database"):
            for p in top_5:
                row = dict(p)
                row["created_utc"] = now_utc_iso()
                row["sharp_odds_json"] = p["sharp_odds_json"]
                db_insert_pick(row)
            st.success("Logged Top 5. Go to History tab.")

with tabs[1]:
    st.subheader("History (your proprietary dataset)")
    rows = db_recent(limit=300)
    if not rows:
        st.info("No picks logged yet. Go to Scanner → Run Scan → Log Top 5.")
    else:
        # Show compact table
        display = []
        for r in rows:
            display.append({
                "id": r["id"],
                "created_utc": r["created_utc"],
                "sport": r["sport_key"],
                "event": r["event_id"][:8] if r["event_id"] else None,
                "selection": r["selection"],
                "book": r["book"],
                "odds": r["odds"],
                "EV%": round(r["ev_pct"], 2),
                "closing_odds": r["closing_odds"],
                "CLV": r["clv"],
            })
        st.dataframe(display, use_container_width=True)

with tabs[2]:
    st.subheader("CLV Update (turn picks into proof)")
    st.caption("This updates ‘closing-ish’ odds using Pinnacle at time of update. It’s not perfect close, but it’s consistent and measurable.")

    rows = db_events_needing_closing(limit=200)
    st.write(f"Pending picks without closing odds: **{len(rows)}**")

    minutes_before = st.number_input("Only update events starting within X minutes", value=180, step=30)

    if st.button("🔄 Update Closing Odds + CLV"):
        updated = 0
        skipped = 0
        errors = 0

        now = datetime.now(timezone.utc)

        for r in rows:
            try:
                commence = parse_commence_time(r["commence_utc"])
                mins_to = (commence - now).total_seconds() / 60.0

                # Only update near start time (so it behaves like “closing”)
                if mins_to > float(minutes_before):
                    skipped += 1
                    continue

                closing = pick_closing_odds_for_selection(
                    api_key=api_key,
                    sport_key=r["sport_key"],
                    event_id=r["event_id"],
                    selection=r["selection"]
                )
                if closing is None:
                    skipped += 1
                    continue

                # CLV for decimal odds: (1/closing) - (1/entry) is probability improvement
                # Positive CLV means you beat the market (good).
                entry_odds = float(db_conn().execute("SELECT odds FROM picks WHERE id=?", (r["id"],)).fetchone()[0])
                clv = (1.0 / closing) - (1.0 / entry_odds)

                db_set_closing(int(r["id"]), float(closing), float(clv))
                updated += 1

            except Exception:
                errors += 1

        st.success(f"Updated: {updated} | Skipped: {skipped} | Errors: {errors}")
        st.info("Go to History tab and check CLV. Positive CLV consistently = real edge.")
