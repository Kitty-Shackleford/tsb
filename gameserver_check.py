import json
import os
import requests

API_KEY = os.getenv("NITRADO_TOKEN")  # Ensure this is set before running

# Make the API call
response = requests.get('https://api.nitrado.net/services', headers={'Authorization': f'Bearer {API_KEY}'})

if response.ok:
    data = response.json()
    services = data.get("data", {}).get("services", [])

    # Clean the server names
    for service in services:
        if 'details' in service:
            service_name = service['details'].get('name', '')
            clean_name = service_name.replace('\u0001', '')  # Remove unwanted characters
            service['details']['name'] = clean_name

    # Output the cleaned data
    print(json.dumps(data, indent=4))
else:
    print(f"Error: {response.status_code}, {response.text}")
