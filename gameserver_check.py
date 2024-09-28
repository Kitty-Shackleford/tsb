import json
import os
import requests

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

# Function to get gameserver details for a given service ID
def get_gameserver_details(service_id):
    response = requests.get(f'https://api.nitrado.net/services/{service_id}/gameservers', headers={'Authorization': f'Bearer {API_KEY}'})
    if response.ok:
        return response.json().get("data", {}).get("gameserver", {})
    else:
        print(f"Error fetching gameserver details for service ID {service_id}: {response.status_code} - {response.text}")
        return {}

# Fetch all services
services = get_services()

# Prepare Markdown output
markdown_output = "# Gameserver Details\n\n"

# Loop through each service and fetch its gameserver details
for service in services:
    service_id = service.get("id")
    gameserver = get_gameserver_details(service_id)

    if gameserver:
        markdown_output += f"## Service ID: {service_id}\n\n"
        markdown_output += "| Property | Value |\n"
        markdown_output += "|----------|-------|\n"

        properties = {
            "Username": service.get("username"),
            "Status": gameserver.get("status"),
            "IP Address": gameserver.get("ip"),
            "Port": gameserver.get("port"),
            "Game": gameserver.get("game_human"),
            "Slots": gameserver.get("slots"),
            "Location": service.get("location_id"),
            "Start Date": service.get("start_date"),
            "Comment": service.get("comment"),
        }

        for key, value in properties.items():
            markdown_output += f"| {key} | {value} |\n"

        markdown_output += "\n"

# Output the Markdown formatted result
print(markdown_output)
