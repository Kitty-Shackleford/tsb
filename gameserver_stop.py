import json
import os
import requests

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

# Function to stop gameserver
def stop_gameserver(nitrado_id, stop_message=None):
    url = f'https://api.nitrado.net/services/{nitrado_id}/gameservers/stop'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {}
    
    if stop_message:
        data['stop_message'] = stop_message

    response = requests.post(url, headers=headers, json=data)
    
    if response.ok:
        print(f"Gameserver for NITRADO_ID {nitrado_id} has been stopped successfully.")
        print(response.json())  # Print the success response
    else:
        print(f"Error stopping gameserver for NITRADO_ID {nitrado_id}: {response.status_code} - {response.text}")

# Example of stopping a gameserver
# You can provide a stop message if needed
stop_gameserver(NITRADO_ID, "Stopping the server for maintenance.")
