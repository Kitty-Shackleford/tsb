import json
import os
import requests
import re

# Ensure the API key is set
API_KEY = os.getenv("NITRADO_TOKEN")
if not API_KEY:
    print("Error: NITRADO_TOKEN environment variable is not set.")
    exit(1)

# Function to get all services
def get_services():
    response = requests.get('https://api.nitrado.net/services', headers={'Authorization': f'Bearer {API_KEY}'})
    if response.ok:
        return response.json().get("data", {}).get("services", [])
    else:
        print(f"Error fetching services: {response.status_code} - {response.text}")
        return []

# Prepare Markdown output
markdown_output = "# Gameserver Details\n\n"

# Fetch all services
services = get_services()

# Loop through each service and fetch its gameserver details
for service in services:
    service_id = service.get("id")
    response = requests.get(f'https://api.nitrado.net/services/{service_id}/gameservers', headers={'Authorization': f'Bearer {API_KEY}'})
    
    if response.ok:
        gameserver = response.json().get("data", {}).get("gameserver", {})
        
        if gameserver:
            # Get server name from the query section
            server_name = gameserver.get("query", {}).get("server_name", "Server Name Not Available")
            # Clean server name to exclude null characters and spaces
            server_name = re.sub(r'[^a-zA-Z]', '', server_name) or "Server Name Not Available"
            markdown_output += f"## {server_name}\n\n"

            markdown_output += "| Property        | Value                   |\n"
            markdown_output += "|-----------------|-------------------------|\n"

            # Calculate player count
            player_count = gameserver.get("query", {}).get("player_current", 0)
            max_slots = gameserver.get("slots", 0)

            properties = {
                "Status": gameserver.get("status", "Unknown"),
                "Player Count": f"{player_count}/{max_slots}",
                "Last Update": gameserver.get("game_specific", {}).get("last_update", "None"),
                "Comment": service.get("comment", "None"),
                "Banned Users": ", ".join(gameserver.get("general", {}).get("bans", "").splitlines() if gameserver.get("general", {}).get("bans") else []),
                "Game": gameserver.get("game_human", "Unknown"),
                "Mission": gameserver.get("settings", {}).get("config", {}).get("mission", "Unknown"),
                "3rd Person": "Enabled" if gameserver.get("settings", {}).get("config", {}).get("disable3rdPerson", "1") == "0" else "Disabled",
                "Crosshair": "Enabled" if gameserver.get("settings", {}).get("config", {}).get("disableCrosshair", "1") == "0" else "Disabled",
                "Shot Validation": "Enabled" if gameserver.get("settings", {}).get("config", {}).get("shotValidation", "0") == "1" else "Disabled",
                "Mouse and Keyboard": "Enabled" if gameserver.get("settings", {}).get("config", {}).get("enableMouseAndKeyboard", "1") == "1" else "Disabled",
                "Whitelist": "Enabled" if gameserver.get("settings", {}).get("config", {}).get("enableWhitelist", "1") == "1" else "Disabled",
                "Base Damage": "Enabled" if gameserver.get("settings", {}).get("config", {}).get("disableBaseDamage", "1") == "0" else "Disabled",
                "Container Damage": "Enabled" if gameserver.get("settings", {}).get("config", {}).get("disableContainerDamage", "1") == "0" else "Disabled",
                "Priority": gameserver.get("settings", {}).get("general", {}).get("priority", "None").replace('\r\n', ', '),
                "Whitelist": gameserver.get("settings", {}).get("general", {}).get("whitelist", "None").replace('\r\n', ', '),
                "Version": gameserver.get("query", {}).get("version", "Unknown"),
            }

            for key, value in properties.items():
                markdown_output += f"| {key} | {value} |\n"

            markdown_output += "\n"
    else:
        print(f"Error fetching gameserver details for service ID {service_id}: {response.status_code} - {response.text}")

# Output the Markdown formatted result
print(markdown_output)
