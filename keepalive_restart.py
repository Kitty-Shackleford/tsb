import os
import requests
import sys

# Ensure the API key and ID are set
API_KEY = os.getenv("NITRADO_TOKEN")
NITRADO_ID = os.getenv("NITRADO_ID")

if not API_KEY or not NITRADO_ID:
    print("Error: NITRADO_TOKEN or NITRADO_ID environment variable is not set.")
    sys.exit(1)

# Function to restart the server
def restart_server():
    url = f"https://api.nitrado.net/services/{NITRADO_ID}/gameservers/restart"
    response = requests.post(url, headers={'Authorization': f'Bearer {API_KEY}'})

    if response.ok:
        print("Server restart initiated successfully.")
    else:
        print(f"Error restarting server: {response.status_code} - {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    restart_server()

