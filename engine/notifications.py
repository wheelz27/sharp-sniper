import requests
import json
import config

def send_sniper_alert(top_plays, parlay_odds="+264"):
    """Sends the top 2 plays to your Discord channel via Webhook"""
    if not top_plays or len(top_plays) < 2:
        return

    p1, p2 = top_plays[0], top_plays[1]
    
    payload = {
        "username": "EDGEINTEL SNIPER",
        "embeds": [{
            "title": "🎯 NEW SNIPER PARLAY IDENTIFIED",
            "description": f"**Total Odds: {parlay_odds}**\nCombined Edge: {round(p1.spread_edge + p2.spread_edge, 1)} pts",
            "color": 3066993, # Green
            "fields": [
                {"name": f"1. {p1.play_side} ({p1.market_spread_home:+.1f})", "value": f"{p1.away_team} @ {p1.home_team}", "inline": False},
                {"name": f"2. {p2.play_side} ({p2.market_spread_home:+.1f})", "value": f"{p2.away_team} @ {p2.home_team}", "inline": False}
            ],
            "footer": {"text": "EdgeIntel Command Center | Automated Alert"}
        }]
    }

    # Use the Webhook URL from your Streamlit Secrets or config.py
    webhook_url = getattr(config, 'DISCORD_WEBHOOK_URL', None)
    if webhook_url:
        requests.post(webhook_url, json=payload)
