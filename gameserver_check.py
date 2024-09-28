import requests
import os

API_KEY = os.environ.get("NITRADO_TOKEN")  # Use the environment variable for the API key

def get_services():
    response = requests.get("https://api.nitrado.net/services", headers={"Authorization": f"Bearer {API_KEY}"})
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()['data']  # Ensure we are returning the expected 'data'

def get_gameserver_details(service_id):
    response = requests.get(f"https://api.nitrado.net/services/{service_id}/gameservers", headers={"Authorization": f"Bearer {API_KEY}"})
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def format_summary(data):
    gameserver = data['data']['gameserver']
    current_players = gameserver['query']['player_current']
    max_slots = gameserver['slots']
    
    summary = f"""
## Gameserver Details

- **Service ID:** {data['data']['service_id']}
- **Status:** {gameserver['status']}
- **Username:** {gameserver['username']}
- **IP Address:** {gameserver['ip']}
- **Port:** {gameserver['port']}
- **Slots:** {max_slots}
- **Current Players:** {current_players} / {max_slots}
- **Game:** {gameserver['game_human']}

### Host Systems
"""
    for os_type, details in gameserver['hostsystems'].items():
        summary += f"- **{os_type.capitalize()}:**\n"
        summary += f"  - Hostname: {details['hostname']}\n"
        summary += f"  - Status: {details['status']}\n"

    summary += f"""
### Memory
- **Type:** {gameserver['memory']}
- **Memory (MB):** {gameserver['memory_mb']}

### Game Specific Details
- **Path:** {gameserver['game_specific']['path']}
- **Update Status:** {gameserver['game_specific']['update_status']}
- **Last Update:** {gameserver['game_specific']['last_update']}
- **Features:**
  - Backups: {'Yes' if gameserver['game_specific']['features']['has_backups'] else 'No'}
  - RCON: {'Yes' if gameserver['game_specific']['features']['has_rcon'] else 'No'}
  - FTP: {'Yes' if gameserver['game_specific']['features']['has_ftp'] else 'No'}
  - Database: {'Yes' if gameserver['game_specific']['features']['has_database'] else 'No'}

### Settings
- **Hostname:** (obfuscated)
- **Admin Password:** (obfuscated)
- **Mission:** {gameserver['settings']['general']['mission']}

### Query Information
- **Server Name:** (obfuscated)
- **Connect IP:** {gameserver['query']['connect_ip']}
- **Map:** {gameserver['query']['map']}
- **Version:** {gameserver['query']['version']}
"""
    return summary

if __name__ == "__main__":
    try:
        services = get_services()
        if not isinstance(services, list):
            raise ValueError("The services data is not formatted correctly: expected a list.")

        all_summaries = []

        for service in services:
            service_id = service['id']
            try:
                gameserver_data = get_gameserver_details(service_id)
                summary = format_summary(gameserver_data)
                all_summaries.append(summary)
            except Exception as e:
                print(f"Error fetching data for service ID {service_id}: {e}")

        # Write all summaries to the output file
        with open("output.md", "w") as f:
            f.write("\n\n---\n\n".join(all_summaries))

    except Exception as e:
        print(f"An error occurred: {e}")
