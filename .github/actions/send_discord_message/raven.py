import os
import requests
import sys

# Get summary from input
summary = os.getenv('INPUT_SUMMARY')

# Discord webhook URL
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')  # You can also pass this as an input

# Prepare the payload
data = {
    "content": summary
}

# Send the message
response = requests.post(WEBHOOK_URL, json=data)

if response.status_code != 204:
    print(f"Failed to send message: {response.status_code} - {response.text}")
    sys.exit(1)

