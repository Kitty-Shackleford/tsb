import os
import requests

# Ensure the API key is set
API_KEY = os.getenv("NITRADO_TOKEN")
if not API_KEY:
    print("Error: NITRADO_TOKEN environment variable is not set.")
    exit(1)

# Fetch public service notifications
response = requests.get(
    'https://api.nitrado.net/notification/services',
    headers={'Authorization': f'Bearer {API_KEY}'}
)

# Check the response
if response.ok:
    notifications = response.json().get("data", {}).get("notifications", [])
    
    if notifications:
        print("## Public Service Notifications\n")
        for notification in notifications:
            print(f"### Level: {notification['level']}")
            print(f"**Message:** {notification['message']}\n")
            print(f"- **Product Types:** {', '.join(notification['product_types'])}")
            print(f"- **Locations:** {', '.join(notification['locations'])}\n")
    else:
        print("No notifications found.")
else:
    print(f"Error fetching notifications: {response.status_code} - {response.text}")
