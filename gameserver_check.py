import requests
import os

API_KEY = os.getenv("NITRADO_TOKEN")  # Get API key from environment variable

def get_services():
    response = requests.get("https://api.nitrado.net/services", headers={"Authorization": f"Bearer {API_KEY}"})
    response.raise_for_status()
    data = response.json()

    services = data.get('services', [])
    
    if not isinstance(services, list):
        raise ValueError(f"The services data is not formatted correctly: {data}")  # Log the actual response
    
    return services

def get_gameserver_details(service_id):
    response = requests.get(f"https://api.nitrado.net/services/{service_id}/gameservers", headers={"Authorization": f"Bearer {API_KEY}"})
    response.raise_for_status()
    return response.json()

def format_summary(data):
    gameserver = data.get('data', {}).get('gameserver', {})
    current_players = gameserver.get('query', {}).get('player_current', 0)  # Default to 0 if null
    max_slots = gameserver.get('slots', 0)  # Default to 0 if null

    # Handle potential null or missing values
    summary = f"""
## Gameserver Details

- **Service ID:** {data['data'].get('service_id', 'N/A')}
- **Status:** {gameserver.get('status', 'N/A')}
- **Username:** {gameserver.get('username', 'N/A')}
- **IP Address:** {gameserver.get('ip', 'N/A')}
- **Port:** {gameserver.get('port', 'N/A')}
- **Slots:** {max_slots}
- **Current Players:** {current_players} / {max_slots}
- **Game:** {gameserver.get('game_human', 'N/A')}
"""
    return summary

if __name__ == "__main__":
    all_summaries = []
    errors = []

    try:
        services = get_services()
        for service in services:
            service_id = service.get('id')  # Safely get the service ID
            try:
                gameserver_data = get_gameserver_details(service_id)
                summary = format_summary(gameserver_data)
                all_summaries.append(summary)
            except Exception as e:
                error_message = f"Error fetching data for service ID {service_id}: {e}"
                errors.append(error_message)

    except Exception as e:
        errors.append(f"An error occurred while fetching services: {e}")

    # Write all summaries to the output file
    with open("output.md", "w") as f:
        if all_summaries:
            f.write("\n\n---\n\n".join(all_summaries))
        else:
            f.write("No gameserver details available.")

        if errors:
            f.write("\n\n### Errors\n")
            f.write("\n".join(errors))
