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

# Optional messages
message = "Restarting the server"
restart_message = "Server is restarting..."

# Prepare the API request
url = f'https://api.nitrado.net/services/{NITRADO_ID}/gameservers/restart'
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
payload = {
    'message': message,
    'restart_message': restart_message
}

# Make the request to restart the server
response = requests.post(url, headers=headers, json=payload)

# Handle the response
if response.ok:
    print("Success:", response.json())
else:
    print(f"Error restarting gameserver: {response.status_code} - {response.text}")
