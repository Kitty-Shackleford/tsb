import os
import requests
import sys
from datetime import datetime

# Ensure the API key and ID are set
API_KEY = os.getenv("NITRADO_TOKEN")
NITRADO_ID = os.getenv("NITRADO_ID")

if not API_KEY or not NITRADO_ID:
    print("Error: NITRADO_TOKEN or NITRADO_ID environment variable is not set.")
    sys.exit(1)

# Function to get server details
def get_server_details():
    url = f"https://api.nitrado.net/services/{NITRADO_ID}/gameservers"
    response = requests.get(url, headers={'Authorization': f'Bearer {API_KEY}'})
    
    if response.ok:
        return response.json().get("data", {}).get("gameserver", {})
    else:
        print(f"Error fetching server details: {response.status_code} - {response.text}")
        sys.exit(1)

# Function to restart the server
def restart_server():
    url = f"https://api.nitrado.net/services/{NITRADO_ID}/gameservers/restart"
    response = requests.post(url, headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'})
    
    if response.ok:
        print("Server is being restarted.")
    else:
        print(f"Error restarting server: {response.status_code} - {response.text}")
        sys.exit(1)

# Function to calculate uptime
def calculate_uptime(last_restart):
    last_restart_time = datetime.fromisoformat(last_restart.replace("Z", "+00:00"))
    uptime = datetime.utcnow() - last_restart_time
    return uptime

if __name__ == "__main__":
    gameserver = get_server_details()
    status = gameserver.get("status", "unknown")
    
    print(f"Current Server Status: {status}")  # Output status for GitHub Actions

    last_restart = gameserver.get("game_specific", {}).get("last_restart", "unknown")
    uptime = "N/A"
    
    if status == "started":
        if last_restart != "unknown":
            uptime = calculate_uptime(last_restart)
            print(f"Server is running. Uptime: {uptime}")
        else:
            print("Last restart time is unknown.")
    elif status == "stopped":
        restart_server()
    else:
        print(f"Unexpected server status: {status}")

    # Markdown Summary Output
    with open("summary.md", "w") as summary_file:
        summary_file.write("## Summary\n")
        summary_file.write(f"- **Status**: {status}\n")
        summary_file.write(f"- **Last Restart**: {last_restart if last_restart != 'unknown' else 'N/A'}\n")
        summary_file.write(f"- **Uptime**: {str(uptime) if last_restart != 'unknown' else 'N/A'}\n")
