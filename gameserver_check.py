import requests
import os

API_KEY = os.getenv("NITRADO_TOKEN")  # Get API key from environment variable

def clean_text(text):
    return text.replace('\u0001', ' ').replace('\x01', ' ').strip()  # Replace control characters with a space

def get_services():
    response = requests.get("https://api.nitrado.net/services", headers={"Authorization": f"Bearer {API_KEY}"})
    response.raise_for_status()
    data = response.json().get('data', [])
    
    if not isinstance(data, list):
        raise ValueError(f"The services data is not formatted correctly: {data}")  # Log the actual response
    
    return data

def get_gameserver_details(service_id):
    response = requests.get(f"https://api.nitrado.net/services/{service_id}/gameservers", headers={"Authorization": f"Bearer {API_KEY}"})
    response.raise_for_status()
    gameserver_data = response.json()

    # Clean the gameserver details immediately after fetching
    gameserver_data['data']['gameserver']['username'] = clean_text(gameserver_data['data']['gameserver']['username'])
    gameserver_data['data']['gameserver']['game_human'] = clean_text(gameserver_data['data']['gameserver']['game_human'])
    gameserver_data['data']['gameserver']['details']['address'] = clean_text(gameserver_data['data']['gameserver']['details']['address'])
    gameserver_data['data']['gameserver']['details']['name'] = clean_text(gameserver_data['data']['gameserver']['details']['name'])
    
    return gameserver_data

def format_summary(data):
    gameserver = data['data']['gameserver']
    current_players = gameserver['query']['player_current']
    max_slots = gameserver['slots']
    
    summary = f"""
## Gameserver Details

- **Service ID:** {data['data']['service_id']}
- **Status:** {gameserver['status']}
- **Username:** {gameserver['username']}
- **IP Address:** {gameserver['details']['address']}
- **Port:** {gameserver['port']}
- **Slots:** {max_slots}
- **Current Players:** {current_players} / {max_slots}
- **Game:** {gameserver['game_human']}
- **Server Name:** {gameserver['details']['name']}
"""
    return summary.strip()

if __name__ == "__main__":
    all_summaries = []
    errors = []

    try:
        services = get_services()
        if isinstance(services, dict) and 'services' in services:
            services = services['services']  # Adjust this if necessary

        for service in services:
            service_id = service['id']
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

    print("Output written to output.md")
