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
    # Use lowercase username for the dictionary key (easier for the mod to find)
    username_key = player["username"].lower()
    
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

    # Add the NEW line to the existing player data
    if best_modes:
        player["highest_tier_mode"] = random.choice(best_modes)
    else:
        player["highest_tier_mode"] = None

    # Save the whole player object exactly as it came from the API
    player_tiers[username_key] = player

# Save to JSON
with open('tiers.json', 'w') as file:
    json.dump(player_tiers, file, indent=4)

print(f"Success! Processed {len(player_tiers)} players.")
