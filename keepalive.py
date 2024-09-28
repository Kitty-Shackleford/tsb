import os
import requests
import sys

# Ensure the API key and ID are set
API_KEY = os.getenv("NITRADO_TOKEN")
NITRADO_ID = os.getenv("NITRADO_ID")

if not API_KEY or not NITRADO_ID:
    print("Error: NITRADO_TOKEN or NITRADO_ID environment variable is not set.")
    sys.exit(1)

# Function to get server status
def get_server_status():
    url = f"https://api.nitrado.net/services/{NITRADO_ID}/gameservers"
    response = requests.get(url, headers={'Authorization': f'Bearer {API_KEY}'})
    
    if response.ok:
        gameserver = response.json().get("data", {}).get("gameserver", {})
        status = gameserver.get("status", "unknown")
        return status
    else:
        print(f"Error fetching server status: {response.status_code} - {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    status = get_server_status()
    print(status)  # Output status for GitHub Actions
