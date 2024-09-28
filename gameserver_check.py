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

# Function to get all services
def get_services():
    response = requests.get('https://api.nitrado.net/services', headers={'Authorization': f'Bearer {API_KEY}'})
    if response.ok:
        return response.json().get("data", {}).get("services", [])
    else:
        print(f"Error fetching services: {response.status_code} - {response.text}")
        return []

# Function to get gameserver details for a given service ID
def get_gameserver_details(service_id):
    response = requests.get(f'https://api.nitrado.net/services/{service_id}/gameservers', headers={'Authorization': f'Bearer {API_KEY}'})
    if response.ok:
        return response.json().get("data", {}).get("gameserver", {})
    else:
        print(f"Error fetching gameserver details for service ID {service_id}: {response.status_code} - {response.text}")
        return {}

# Prepare Markdown output
markdown_output = "# Gameserver Details\n\n"

# Fetch gameserver details using NITRADO_ID if available
if NITRADO_ID:
    gameserver = get_gameserver_details(NITRADO_ID)
    services = [{"id": NITRADO_ID, "comment": ""}]  # Create a dummy service entry for this ID
else:
    # Fetch all services
    services = get_services()

# Loop through each service and fetch its gameserver details
for service in services:
    service_id = service.get("id")
    gameserver = get_gameserver_details(service_id)

    if gameserver:
        server_name = gameserver.get("details", {}).get("name", "")
        if server_name:
            markdown_output += f"## {server_name}\n\n"
        else:
            markdown_output += f"## \n\n"  # Empty header if no server name

        markdown_output += "| Property        | Value                   |\n"
        markdown_output += "|-----------------|-------------------------|\n"

        # Calculate player count
        player_count = gameserver.get("query", {}).get("player_current", 0)
        max_slots = gameserver.get("slots", 0)

        properties = {
            "Status": gameserver.get("status"),
            "Player Count": f"{player_count}/{max_slots}",
            "Last Update": gameserver.get("game_specific", {}).get("last_update", "None"),
            "Comment": service.get("comment", "None"),
            "Banned Users": ", ".join(gameserver.get("general", {}).get("bans", "").splitlines() if gameserver.get("general", {}).get("bans") else []),
        }

        for key, value in properties.items():
            markdown_output += f"| {key} | {value} |\n"

        markdown_output += "\n"

# Output the Markdown formatted result
print(markdown_output)
