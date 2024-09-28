import os
import requests

# Ensure the API key and NITRADO_ID are set
API_KEY = os.getenv("NITRADO_TOKEN")
NITRADO_ID = os.getenv("NITRADO_ID")

if not API_KEY or not NITRADO_ID:
    print("Error: NITRADO_TOKEN or NITRADO_ID environment variable is not set.")
    exit(1)

# Define the stop parameters
stop_params = {
    "message": "Stopping server via GitHub Action",
    "stop_message": "The server is stopping now. Please check back later."
}

# Make the POST request to stop the gameserver
response = requests.post(
    f'https://api.nitrado.net/services/{NITRADO_ID}/gameservers/stop',
    headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
    json=stop_params
)

if response.ok:
    print("Success:", response.json())
else:
    print(f"Error stopping gameserver: {response.status_code} - {response.text}")
