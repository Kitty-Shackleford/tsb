import requests
import os

API_KEY = os.environ.get("NITRADO_TOKEN")  # Use the environment variable for the API key

def get_services():
    response = requests.get("https://api.nitrado.net/services", headers={"Authorization": f"Bearer {API_KEY}"})
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()['data']

def get_gameserver_details(service_id):
    response = requests.get(f"https://api.nitrado.net/services/{service_id}/gameservers", headers={"Authorization": f"Bearer {API_KEY}"})
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def format_summary(data):
    gameserver = data['data']['gameserver']
    current_players = gameserver['query']['player_current']
    max_slots = gameserver['slots']
    
    summary = f"Gameserver Details\n\n"
    summary += f"Service ID: {data['data']['service_id']}\n"
    summary += f"Status: {gameserver['status']}\n"
    summary += f"Username: {gameserver['username']}\n"
    summary += f"IP Address: {gameserver['ip']}\n"
    summary += f"Port: {gameserver['port']}\n"
    summary += f"Slots: {max_slots}\n"
    summary += f"Current Players: {current_players} / {max_slots}\n"
    summary += f"Game: {gameserver['game_human']}\n\n"
    
    summary += "Host Systems:\n"
    for os_type, details in gameserver['hostsystems'].items():
        summary += f"- {os_type.capitalize()}:\n"
        summary += f"  - Hostname: {details['hostname']}\n"
        summary += f"  - Status: {details['status']}\n"

    summary += f"\nMemory:\n"
    summary += f"- Type: {gameserver['memory']}\n"
    summary += f"- Memory (MB): {gameserver['memory_mb']}\n"

    summary += f"\nGame Specific Details:\n"
    summary += f"- Path: {gameserver['game_specific']['path']}\n"
    summary += f"- Update Status: {gameserver['game_specific']['update_status']}\n"
    summary += f"- Last Update: {gameserver['game_specific']['last_update']}\n"
    summary += f"- Features:\n"
    summary += f"  - Backups: {'Yes' if gameserver['game_specific']['features']['has_backups'] else 'No'}\n"
    summary += f"  - RCON: {'Yes' if gameserver['game_specific']['features']['has_rcon'] else 'No'}\n"
    summary += f"  - FTP: {'Yes' if gameserver['game_specific']['features']['has_ftp'] else 'No'}\n"
    summary += f"  - Database: {'Yes' if gameserver['game_specific']['features']['has_database'] else 'No'}\n"

    summary += f"\nSettings:\n"
    summary += f"- Hostname: (obfuscated)\n"
    summary += f"- Admin Password: (obfuscated)\n"
    summary += f"- Mission: {gameserver['settings']['general']['mission']}\n"

    summary += f"\nQuery Information:\n"
    summary += f"- Server Name: (obfuscated)\n"
    summary += f"- Connect IP: {gameserver['query']['connect_ip']}\n"
    summary += f"- Map: {gameserver['query']['map']}\n"
    summary += f"- Version: {gameserver['query']['version']}\n"
    
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
                all_summaries.append(f"Error fetching data for service ID {service_id}: {e}")

        # Write all summaries to the output file
        with open("output.txt", "w") as f:
            f.write("\n\n---\n\n".join(all_summaries))

    except Exception as e:
        with open("output.txt", "w") as f:
            f.write(f"An error occurred: {e}")
