import requests
import json
import random

# 1. Get the raw data
url = "https://krtier.xyz/api/ranking/detailed?limit=10000&offset=0"
response = requests.get(url)
data = response.json()

# Tier ranking for the "Highest Tier" logic
tier_rankings = ["HT1", "LT1", "HT2", "LT2", "HT3", "LT3", "HT4", "LT4", "HT5", "LT5"]

player_tiers = {}

for player in data:
    # --- FIX: Convert UUID from no-dashes to dashes ---
    # API gives: "bbd9def08d144c6384229c1c36e816cc"
    # We need:   "bbd9def0-8d14-4c63-8422-9c1c36e816cc"
    raw_uuid = player["uuid"]
    formatted_uuid = f"{raw_uuid[0:8]}-{raw_uuid[8:12]}-{raw_uuid[12:16]}-{raw_uuid[16:20]}-{raw_uuid[20:]}"
    player["uuid_formatted"] = formatted_uuid

    # These are the mode keys exactly as they appear in the API
    modes = ["sword_tier", "axe_tier", "pot_tier", "npot_tier", "uhc_tier", "smp_tier", "cpvp_tier", "mace_tier"]

    best_index = 999
    best_modes = []

    # Find which mode has the best tier string
    for m in modes:
        tier_str = player.get(m)
        if tier_str in tier_rankings:
            idx = tier_rankings.index(tier_str)
            if idx < best_index:
                best_index = idx
                best_modes = [m]
            elif idx == best_index:
                best_modes.append(m)

    # Pick a random mode if tied
    if best_modes:
        player["highest_tier_mode"] = random.choice(best_modes)
    else:
        player["highest_tier_mode"] = None

    # Key by formatted UUID (with dashes) instead of username
    player_tiers[formatted_uuid] = player

# Save to JSON
with open('tiers.json', 'w') as file:
    json.dump(player_tiers, file, indent=4)

print(f"Success! Processed {len(player_tiers)} players.")
