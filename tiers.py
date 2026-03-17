import requests
import json

# 1. We ask for everything all at once! (Limit 10000)
url = "https://krtier.xyz/api/ranking/detailed?limit=10000&offset=0"
print("Fetching all players from krtiers API...")

response = requests.get(url)
data = response.json()

player_tiers = {}

# 2. Loop through every player in the massive list the API gave us
for player in data:
    username = player["username"]
    
    # We create a mini-dictionary just for this player's modes
    player_data = {}
    
    # We save their overall combat rank as their "highest" default
    player_data["highest"] = player["combat_tier"]
    
    # 3. Handling the "null" values!
    # We only add the gamemode to their file if it is NOT null
    if player["sword_tier"] is not None:
        player_data["sword"] = player["sword_tier"]
        
    if player["axe_tier"] is not None:
        player_data["axe"] = player["axe_tier"]
        
    if player["pot_tier"] is not None:
        player_data["pot"] = player["pot_tier"]
        
    if player["cpvp_tier"] is not None:
        player_data["crystal"] = player["cpvp_tier"]
        
    if player["mace_tier"] is not None:
        player_data["mace"] = player["mace_tier"]
        
    if player["smp_tier"] is not None:
        player_data["smp"] = player["smp_tier"]
        
    if player["uhc_tier"] is not None:
        player_data["uhc"] = player["uhc_tier"]

    # 4. Save the player to our main HashMap
    # PRO TIP: We save the username as lowercase (.lower()) so when players type 
    # /krtiers NeOnD, it still finds "NE0ND" without breaking!
    player_tiers[username.lower()] = player_data

# 5. Save it all to a clean JSON file
with open('tiers.json', 'w') as file:
    json.dump(player_tiers, file, indent=4)

print(f"Success! Saved {len(player_tiers)} players to tiers.json")
