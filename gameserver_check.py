import json
import os
import requests
import re

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
markdown_output = "# 🎮 Gameserver Details\n\n"

# Fetch gameserver details for the provided NITRADO_ID
response = requests.get(
    f'https://api.nitrado.net/services/{NITRADO_ID}/gameservers',
    headers={'Authorization': f'Bearer {API_KEY}'}
)

if response.ok:
    gameserver = response.json().get("data", {}).get("gameserver", {})
    
    if gameserver:
        # Get server name from the query section
        server_name = gameserver.get("query", {}).get("server_name", "Server Name Not Available")
        
        # Clean the server name to exclude null characters and spaces
        server_name = re.sub(r'[^a-zA-Z]', '', server_name)
        if not server_name:  # Fallback in case it gets fully cleaned
            server_name = "Server Name Not Available"
        
        # Grouped Server Information
        markdown_output += f"## 🖥️ {server_name}\n\n"

        # General Information Section
        markdown_output += "### 📋 General Information\n\n"
        markdown_output += "| **Property**        | **Value**                  |\n"
        markdown_output += "|---------------------|----------------------------|\n"
        
        general_properties = {
            "Status": gameserver.get("status", "Unknown"),
            "Game": gameserver.get("game_human", "Unknown"),
            "Mission": gameserver.get("settings", {}).get("config", {}).get("mission", "Unknown"),
            "Version": gameserver.get("query", {}).get("version", "Unknown"),
            "Last Update": gameserver.get("game_specific", {}).get("last_update", "None"),
            "Comment": gameserver.get("comment", "None"),
        }

        for key, value in general_properties.items():
            markdown_output += f"| {key} | {value} |\n"
        
        markdown_output += "\n---\n\n"

        # Player Information Section
        markdown_output += "### 👥 Player Information\n\n"
        markdown_output += "| **Property**        | **Value**                  |\n"
        markdown_output += "|---------------------|----------------------------|\n"
        
        player_properties = {
            "Player Count": f"{gameserver.get('query', {}).get('player_current', 0)}/{gameserver.get('slots', 0)}",
            "Banned Users": ", ".join(gameserver.get("general", {}).get("bans", "").splitlines() if gameserver.get("general", {}).get("bans") else []),
        }

        for key, value in player_properties.items():
            markdown_output += f"| {key} | {value} |\n"
        
        markdown_output += "\n---\n\n"

        # Settings Section
        markdown_output += "### ⚙️ Server Settings\n\n"
        markdown_output += "| **Property**        | **Value**                  |\n"
        markdown_output += "|---------------------|----------------------------|\n"
        
        settings_properties = {
            "3rd Person": "✅ Enabled" if gameserver.get("settings", {}).get("config", {}).get("disable3rdPerson", "1") == "0" else "❌ Disabled",
            "Crosshair": "✅ Enabled" if gameserver.get("settings", {}).get("config", {}).get("disableCrosshair", "1") == "0" else "❌ Disabled",
            "Shot Validation": "✅ Enabled" if gameserver.get("settings", {}).get("config", {}).get("shotValidation", "0") == "1" else "❌ Disabled",
            "Mouse and Keyboard": "✅ Enabled" if gameserver.get("settings", {}).get("config", {}).get("enableMouseAndKeyboard", "1") == "1" else "❌ Disabled",
            "Whitelist Feature": "✅ Enabled" if gameserver.get("settings", {}).get("config", {}).get("enableWhitelist", "1") == "1" else "❌ Disabled",
            "Base Damage": "✅ Enabled" if gameserver.get("settings", {}).get("config", {}).get("disableBaseDamage", "1") == "0" else "❌ Disabled",
            "Container Damage": "✅ Enabled" if gameserver.get("settings", {}).get("config", {}).get("disableContainerDamage", "1") == "0" else "❌ Disabled",
            "Priority": gameserver.get("settings", {}).get("general", {}).get("priority", "None").replace('\r\n', ', '),
            "Whitelist": gameserver.get("settings", {}).get("general", {}).get("whitelist", "None").replace('\r\n', ', '),
        }

        for key, value in settings_properties.items():
            markdown_output += f"| {key} | {value} |\n"

        markdown_output += "\n---\n\n"
    else:
        markdown_output += "No gameserver details found for the provided NITRADO_ID.\n"
else:
    markdown_output += f"Error fetching gameserver details for NITRADO_ID {NITRADO_ID}: {response.status_code} - {response.text}\n"

# Output the Markdown formatted result
with open("output.md", "w") as file:
    file.write(markdown_output)
print(markdown_output)
