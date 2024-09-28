import requests
import os

class NitradoAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.nitrado.net/gameserver/details'

    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def get_gameserver_details(self):
        response = requests.get(self.base_url, headers=self._get_headers())
        return response.json()

# Map for status codes and their descriptions
status_descriptions = {
    "started": "The Server is up and running.",
    "stopped": "The Server is stopped.",
    "stopping": "The Server is currently stopping.",
    "restarting": "The Server is currently restarting. This can take some minutes.",
    "suspended": "The server is suspended, which means it needs to be reactivated on the website.",
    "guardian_locked": "Your services are guardian protected, you are currently outside of the allowed times.",
    "gs_installation": "The server is currently performing a game switching action.",
    "backup_restore": "A backup will be restored now.",
    "backup_creation": "A new backup will be created now.",
    "chunkfix": "The Server is running a Minecraft chunkfix.",
    "overviewmap_render": "The Server is running a Minecraft Overview Map rendering."
}

api = NitradoAPI(os.environ['NITRADO_TOKEN'])
gameserver_data = api.get_gameserver_details()

# Generate markdown output
if gameserver_data['status'] == "success":
    gameserver = gameserver_data['data']['gameserver']
    
    markdown_output = "### Gameserver Details\n\n"
    
    # Server basic info
    markdown_output += f"- **Service ID**: {gameserver['service_id']}\n"
    markdown_output += f"- **Username**: {gameserver['username']}\n"
    markdown_output += f"- **Status**: {gameserver['status']} - {status_descriptions.get(gameserver['status'], 'Unknown status.')}\n"
    markdown_output += f"- **IP**: {gameserver['ip']} (IPv6: {gameserver['ipv6']})\n"
    markdown_output += f"- **Game**: {gameserver['game_human']} ({gameserver['game']})\n"
    markdown_output += f"- **Type**: {gameserver['type']}\n"
    markdown_output += f"- **Memory**: {gameserver['memory']} ({gameserver['memory_mb']} MB)\n"
    
    # Player info
    current_players = gameserver['query']['player_current']
    max_slots = gameserver['slots']
    markdown_output += f"- **Slots**: {current_players}/{max_slots}\n"
    markdown_output += f"- **Location**: {gameserver['location']}\n"

    markdown_output += "#### Players:\n"
    if current_players > 0:
        for player in gameserver['query']['players']:
            markdown_output += f"- **Player ID**: {player['id']}, Name: {player['name']}, Score: {player['score']}, Time: {player['time']} seconds, Ping: {player['ping']} ms\n"
    else:
        markdown_output += "No players currently online.\n"

    # Features
    markdown_output += "#### Features:\n"
    features = gameserver['game_specific']['features']
    for feature, available in features.items():
        markdown_output += f"- **{feature.replace('_', ' ').title()}**: {'Yes' if available else 'No'}\n"

    # Quota
    markdown_output += "#### Quota:\n"
    quota = gameserver['quota']
    markdown_output += f"- **Block Usage**: {quota['block_usage']} / {quota['block_hardlimit']} bytes\n"
    markdown_output += f"- **File Usage**: {quota['file_usage']} / {quota['file_hardlimit']} files\n"

else:
    markdown_output = f"Error fetching gameserver details: {gameserver_data.get('message', 'Unknown error')}"

print(markdown_output)
