import json
import os
import requests

# Ensure the API key is set
API_KEY = os.getenv("NITRADO_TOKEN")
if not API_KEY:
    print("Error: NITRADO_TOKEN environment variable is not set.")
    exit(1)

# Make the API call
response = requests.get('https://api.nitrado.net/services', headers={'Authorization': f'Bearer {API_KEY}'})

if response.ok:
    data = response.json()
    gameserver = data.get("data", {}).get("gameserver", {})

    # Prepare Markdown output
    markdown_output = "# Gameserver Details\n\n"
    markdown_output += "| Property | Value |\n"
    markdown_output += "|----------|-------|\n"

    # Extract relevant information
    properties = {
        "Service ID": gameserver.get("service_id"),
        "Username": gameserver.get("username"),
        "Status": gameserver.get("status"),
        "IP Address": gameserver.get("ip"),
        "Port": gameserver.get("port"),
        "Game": gameserver.get("game_human"),
        "Location": gameserver.get("location"),
        "Memory": f"{gameserver.get('memory_mb')} MB",
        "Max Players": gameserver.get("slots"),
        "Last Status Change": gameserver.get("last_status_change"),
        "Connect IP": gameserver.get("query", {}).get("connect_ip"),
        "Current Players": gameserver.get("query", {}).get("player_current"),
        "Max Players": gameserver.get("query", {}).get("player_max"),
    }

    # Format properties into the Markdown table
    for key, value in properties.items():
        markdown_output += f"| {key} | {value} |\n"

    # Output the Markdown formatted result
    print(markdown_output)
else:
    # More detailed error logging based on status code
    if response.status_code == 401:
        print("Error: Unauthorized. Check your API token.")
    elif response.status_code == 404:
        print("Error: API endpoint not found.")
    elif response.status_code == 500:
        print("Error: Server error. Please try again later.")
    else:
        print(f"Error: {response.status_code}, {response.text}")
