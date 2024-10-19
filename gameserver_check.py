import json
import os
import requests
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_env_var(var_name):
    value = os.getenv(var_name)
    if not value:
        logging.error(f"Error: {var_name} environment variable is not set.")
        exit(1)
    return value

def fetch_gameserver_details(nitrado_id, api_key):
    try:
        response = requests.get(
            f'https://api.nitrado.net/services/{nitrado_id}/gameservers',
            headers={'Authorization': f'Bearer {api_key}'},
            timeout=10  # Set a timeout for the request
        )
        response.raise_for_status()  # Raise an error for bad responses
        return response.json().get("data", {}).get("gameserver", {})
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching gameserver details: {e}")
        exit(1)

def format_markdown(gameserver):
    markdown_output = "# 🎮 Gameserver Details\n\n"
    
    server_name = re.sub(r'[^a-zA-Z]', '', gameserver.get("query", {}).get("server_name", "Server Name Not Available")) or "Server Name Not Available"
    markdown_output += f"## 🖥️ {server_name}\n\n"
    
    # General Information
    markdown_output += "### 📋 General Information\n\n"
    general_properties = {
        "Status": gameserver.get("status", "Unknown"),
        "Game": gameserver.get("game_human", "Unknown"),
        "Mission": gameserver.get("settings", {}).get("config", {}).get("mission", "Unknown"),
        "Version": gameserver.get("query", {}).get("version", "Unknown"),
        "Last Update": gameserver.get("game_specific", {}).get("last_update", "None"),
        "Comment": gameserver.get("comment", "None"),
    }
    markdown_output += "| **Property**        | **Value**                  |\n"
    markdown_output += "|---------------------|----------------------------|\n"
    for key, value in general_properties.items():
        markdown_output += f"| {key} | {value} |\n"
    
    # Player Information
    markdown_output += "\n### 👥 Player Information\n\n"
    player_properties = {
        "Player Count": f"{gameserver.get('query', {}).get('player_current', 0)}/{gameserver.get('slots', 0)}",
        "Banned Users": ", ".join(gameserver.get("general", {}).get("bans", "").splitlines()) or "None",
    }
    markdown_output += "| **Property**        | **Value**                  |\n"
    markdown_output += "|---------------------|----------------------------|\n"
    for key, value in player_properties.items():
        markdown_output += f"| {key} | {value} |\n"

    # Server Settings
    markdown_output += "\n### ⚙️ Server Settings\n\n"
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
    markdown_output += "| **Property**        | **Value**                  |\n"
    markdown_output += "|---------------------|----------------------------|\n"
    for key, value in settings_properties.items():
        markdown_output += f"| {key} | {value} |\n"

    return markdown_output

def write_output_to_file(output):
    os.makedirs("output", exist_ok=True)  # Create output directory if it doesn't exist
    with open("output/output.md", "w") as file:
        file.write(output)

def main():
    api_key = get_env_var("NITRADO_TOKEN")
    nitrado_id = get_env_var("NITRADO_ID")
    gameserver = fetch_gameserver_details(nitrado_id, api_key)

    if gameserver:
        markdown_output = format_markdown(gameserver)
        write_output_to_file(markdown_output)
        print(markdown_output)
    else:
        logging.error("No gameserver details found.")

if __name__ == "__main__":
    main()
