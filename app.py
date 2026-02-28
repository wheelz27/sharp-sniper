import streamlit as st
import requests

st.set_page_config(page_title="Sharp Sniper", page_icon="🎯")

st.title("🎯 The Last Shot: Sharp Sniper")

# ---------- CONFIG ----------
SPORT = "basketball_nba"
REGIONS = "us"
MARKETS = "h2h"
MIN_EV = 2.0

# ---------- GET API KEY ----------
try:
    API_KEY = st.secrets["THE_ODDS_API_KEY"]
except Exception:
    st.error("Missing THE_ODDS_API_KEY in Streamlit Secrets.")
    st.stop()

# ---------- BUILD URL ----------
url = (
    f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds"
    f"?apiKey={API_KEY}&regions={REGIONS}&markets={MARKETS}"
)

# ---------- REQUEST ----------
resp = requests.get(url, timeout=20)

st.write("Odds API status:", resp.status_code)

if resp.status_code != 200:
    st.error(resp.text[:1500])
    st.stop()

data = resp.json()

# ---------- EDGE CALC ----------
def devig(odds_list):
    implied = [1 / o for o in odds_list]
    total = sum(implied)
    return [(1 / o) / total for o in odds_list]

all_picks = []

for game in data:
    book = next(
        (b for b in game["bookmakers"] if b["key"] == "pinnacle"),
        None,
    )
    if not book:
        continue

    outcomes = book["markets"][0]["outcomes"]
    odds = [o["price"] for o in outcomes]
    true_probs = devig(odds)

    for outcome, prob in zip(outcomes, true_probs):
        ev = (prob * outcome["price"] - 1) * 100
        if ev >= MIN_EV:
            all_picks.append({
                "game": f"{game['home_team']} vs {game['away_team']}",
                "pick": outcome["name"],
                "odds": outcome["price"],
                "ev": round(ev, 2),
            })

# ---------- DISPLAY ----------
if not all_picks:
    st.warning("No +EV picks found.")
else:
    st.subheader("🔥 +EV Picks")
    for pick in sorted(all_picks, key=lambda x: x["ev"], reverse=True):
        st.success(
            f"{pick['game']} — {pick['pick']} @ {pick['odds']} | EV: {pick['ev']}%"
        )
