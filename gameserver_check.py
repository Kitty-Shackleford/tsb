import json
import os
import requests

# Ensure the API key is set
API_KEY = os.getenv("NITRADO_TOKEN")
if not API_KEY:
    print("Error: NITRADO_TOKEN environment variable is not set.")
    exit(1)

# Check for NITRADO_ID
NITRADO_ID = os.getenv("NITRADO_ID")
if not NITRADO_ID:
    print("Error: NITRADO_ID environment variable is not set.")
    exit(1)

# Prepare Markdown output
markdown_output = "# Gameserver Details\n\n"

# Fetch gameserver details for the provided NITRADO_ID
response = requests.get(
    f'https://api.nitrado.net/services/{NITRADO_ID}/gameservers',
    headers={'Authorization': f'Bearer {API_KEY}'}
)

if response.ok:
    gameserver = response.json().get("data", {}).get("gameserver", {})
    
    if gameserver:
        server_name = gameserver.get("details", {}).get("name", "Server Name Not Available")
        markdown_output += f"## {server_name}\n\n"

        markdown_output += "| Property        | Value                   |\n"
        markdown_output += "|-----------------|-------------------------|\n"

        # Calculate player count
        player_count = gameserver.get("query", {}).get("player_current", 0)
        max_slots = gameserver.get("slots", 0)

        properties = {
            "Status": gameserver.get("status"),
            "Player Count": f"{player_count}/{max_slots}",
            "Last Update": gameserver.get("game_specific", {}).get("last_update", "None"),
            "Comment": gameserver.get("comment", "None"),
            "Banned Users": ", ".join(gameserver.get("general", {}).get("bans", "").splitlines() if gameserver.get("general", {}).get("bans") else []),
        }

        for key, value in properties.items():
            markdown_output += f"| {key} | {value} |\n"

        markdown_output += "\n"
    else:
        print("No gameserver details found for the provided NITRADO_ID.")
else:
    print(f"Error fetching gameserver details for NITRADO_ID {NITRADO_ID}: {response.status_code} - {response.text}")

# Output the Markdown formatted result
print(markdown_output)
