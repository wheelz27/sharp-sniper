import streamlit as st
import requests

# --- CONFIGURATION ---
API_KEY = 'YOUR_API_KEY_HERE' # <--- PASTE YOUR KEY HERE
SPORT = 'upcoming'             # Includes next 8 games across all sports
REGIONS = 'us,eu'              # US for soft books, EU for Pinnacle (Sharp)
MARKETS = 'h2h'                # Moneyline/Match Winner
MAX_EV = 20.0                  # Filters out the 262% glitches
MIN_EV = 2.5                   # Pro-level minimum edge

def de_vig(odds):
    """Strips the bookie fee to find the 'True Probability'"""
    total_implied = sum(1/o for o in odds)
    return [(1/o)/total_implied for o in odds]

st.set_page_config(page_title="Sharp Sniper", page_icon="🎯")
st.title("🎯 The Last Shot: Sharp Sniper")

try:
    url = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds/?apiKey={API_KEY}&regions={REGIONS}&markets={MARKETS}'
    data = requests.get(url).json()
    
    all_picks = []
    for game in data:
        # 1. Identify Pinnacle as the 'Truth'
        pinnacle = next((b for b in game['bookmakers'] if b['key'] == 'pinnacle'), None)
        if not pinnacle: continue
        
        sharp_outcomes = pinnacle['markets'][0]['outcomes']
        sharp_prices = [o['price'] for o in sharp_outcomes]
        true_probs = de_vig(sharp_prices)
        prob_dict = {o['name']: p for o, p in zip(sharp_outcomes, true_probs)}

        # 2. Find Soft Bookies with "Lags"
        for bookie in game['bookmakers']:
            if bookie['key'] == 'pinnacle': continue
            for outcome in bookie['markets'][0]['outcomes']:
                fair_prob = prob_dict.get(outcome['name'], 0)
                ev = (fair_prob * (outcome['price'] - 1)) - (1 - fair_prob)
                ev_pct = ev * 100
                
                # 3. Apply the Glitch-Proof Filter
                if MIN_EV < ev_pct < MAX_EV:
                    all_picks.append({
                        'Game': f"{game['home_team']} vs {game['away_team']}",
                        'Pick': outcome['name'],
                        'Odds': outcome['price'],
                        'Book': bookie['title'],
                        'EV': round(ev_pct, 2)
                    })

    # 4. Rank and Display the "Daily 5"
    top_5 = sorted(all_picks, key=lambda x: x['EV'], reverse=True)[:5]
    
    col1, col2 = st.columns(2)
    with col1:
        st.header("🏆 The Daily 5")
        for i, p in enumerate(top_5, 1):
            st.success(f"**{i}. {p['Pick']}** (@{p['Odds']})\n\n{p['Book']} | **Edge: {p['EV']}%**")
            
    with col2:
        st.header("🔥 2 Parlays")
        if len(top_5) >= 4:
            st.info(f"**Parlay 1 (Safe):** {top_5[0]['Pick']} + {top_5[1]['Pick']}\n\n**Odds:** {round(top_5[0]['Odds']*top_5[1]['Odds'],2)}")
            st.info(f"**Parlay 2 (Lotto):** {top_5[2]['Pick']} + {top_5[3]['Pick']} + {top_5[4]['Pick']}\n\n**Odds:** {round(top_5[2]['Odds']*top_5[3]['Odds']*top_5[4]['Odds'],2)}")

except Exception as e:
    st.error("API connection failed. Check your Key and Quota.")
