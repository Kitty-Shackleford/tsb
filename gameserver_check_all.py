import json
import os
import requests
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Ensure the API key is set
API_KEY = os.getenv("NITRADO_TOKEN")
if not API_KEY:
    logging.error("Error: NITRADO_TOKEN environment variable is not set.")
    exit(1)

def get_services(api_key):
    """Fetch all services from the Nitrado API."""
    try:
        response = requests.get('https://api.nitrado.net/services', headers={'Authorization': f'Bearer {api_key}'})
        response.raise_for_status()
        return response.json().get("data", {}).get("services", [])
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching services: {e}")
        return []

def fetch_gameserver_details(service_id, api_key):
    """Fetch gameserver details for a given service ID."""
    try:
        response = requests.get(f'https://api.nitrado.net/services/{service_id}/gameservers', headers={'Authorization': f'Bearer {api_key}'})
        response.raise_for_status()
        return response.json().get("data", {}).get("gameserver", {})
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching gameserver details for service ID {service_id}: {e}")
        return {}

def format_server_name(gameserver):
    """Clean and format the server name."""
    server_name = gameserver.get("query", {}).get("server_name", "Server Name Not Available")
    return re.sub(r'[^a-zA-Z0-9 ]', '', server_name) or "Server Name Not Available"

def get_status_message(status):
    """Return a formatted message based on the server status."""
    status_messages = {
        "started": "🟢 **The Server is up and running.**",
        "stopped": "🔴 **The Server is stopped.**",
        "stopping": "🟡 **The Server is currently stopping.**",
        "restarting": "🔄 **The Server is currently restarting. This can take some minutes.**",
        "suspended": "⚠️ **The server is suspended and needs to be reactivated on the website.**",
        "guardian_locked": "🔒 **Currently outside of allowed times due to guardian protection.**",
        "gs_installation": "⚙️ **The server is currently performing a game switching action.**",
        "backup_restore": "📦 **A backup will be restored now.**",
        "backup_creation": "💾 **A new backup will be created now.**",
        "chunkfix": "🗺️ **The server is running a Minecraft chunkfix.**",
        "overviewmap_render": "🖼️ **The server is rendering a Minecraft Overview Map.**",
    }
    return status_messages.get(status, "❓ **Unknown Status**")

def generate_markdown(services, api_key):
    """Generate enhanced Markdown output for the gameserver details."""
    markdown_output = "# 🎮 **Gameserver Details**\n\n"
    markdown_output += "Here are the details for your gameservers hosted on Nitrado. Enjoy the game! 🎉\n\n"

    for service in services:
        service_id = service.get("id")
        gameserver = fetch_gameserver_details(service_id, api_key)

        if gameserver:
            server_name = format_server_name(gameserver)
            markdown_output += f"## 🖥️ **{server_name}**\n\n"

            markdown_output += "| **Property**         | **Value**                   |\n"
            markdown_output += "|----------------------|------------------------------|\n"

            player_count = gameserver.get("query", {}).get("player_current", 0)
            max_slots = gameserver.get("slots", 0)

            properties = {
                "Status": get_status_message(gameserver.get('status', 'Unknown')),
                "Player Count": f"👥 **{player_count}/{max_slots}**",
                "Last Update": f"🕒 **{gameserver.get('game_specific', {}).get('last_update', 'None')}**",
                "Comment": f"💬 **{service.get('comment', 'None')}**",
                "Banned Users": f"🚫 **{', '.join(gameserver.get('general', {}).get('bans', '').splitlines() or ['None'])}**",
                "Game": f"🎮 **{gameserver.get('game_human', 'Unknown')}**",
                "Mission": f"🏆 **{gameserver.get('settings', {}).get('config', {}).get('mission', 'Unknown')}**",
                "3rd Person": "✅ **Enabled**" if gameserver.get("settings", {}).get("config", {}).get("disable3rdPerson", "1") == "0" else "❌ **Disabled**",
                "Crosshair": "✅ **Enabled**" if gameserver.get("settings", {}).get("config", {}).get("disableCrosshair", "1") == "0" else "❌ **Disabled**",
                "Shot Validation": "✅ **Enabled**" if gameserver.get("settings", {}).get("config", {}).get("shotValidation", "0") == "1" else "❌ **Disabled**",
                "Mouse and Keyboard": "✅ **Enabled**" if gameserver.get("settings", {}).get("config", {}).get("enableMouseAndKeyboard", "1") == "1" else "❌ **Disabled**",
                "Whitelist": "✅ **Enabled**" if gameserver.get("settings", {}).get("config", {}).get("enableWhitelist", "1") == "1" else "❌ **Disabled**",
                "Base Damage": "✅ **Enabled**" if gameserver.get("settings", {}).get("config", {}).get("disableBaseDamage", "1") == "0" else "❌ **Disabled**",
                "Container Damage": "✅ **Enabled**" if gameserver.get("settings", {}).get("config", {}).get("disableContainerDamage", "1") == "0" else "❌ **Disabled**",
                "Priority": f"🔝 **{gameserver.get('settings', {}).get('general', {}).get('priority', 'None').replace('\\r\\n', ', ')}**",
                "Whitelist": f"📜 **{gameserver.get('settings', {}).get('general', {}).get('whitelist', 'None').replace('\\r\\n', ', ')}**",
                "Version": f"📅 **{gameserver.get('query', {}).get('version', 'Unknown')}**",
            }

            for key, value in properties.items():
                markdown_output += f"| {key} | {value} |\n"

            markdown_output += "\n---\n\n"
        else:
            logging.warning(f"No gameserver details found for service ID {service_id}.")

    return markdown_output

def main():
    services = get_services(API_KEY)
    markdown_output = generate_markdown(services, API_KEY)
    print(markdown_output)

if __name__ == "__main__":
    main()
