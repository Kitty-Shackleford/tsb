import os
import requests
import sys

# Get the Discord webhook URL from environment variable
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not DISCORD_WEBHOOK_URL:
    print("Error: DISCORD_WEBHOOK_URL environment variable is not set.")
    sys.exit(1)

# Get the summary message from the command-line argument
if len(sys.argv) != 2:
    print("Usage: python send_discord_message.py <summary_message>")
    sys.exit(1)

summary_message = sys.argv[1]

# Send the message to Discord
response = requests.post(
    DISCORD_WEBHOOK_URL,
    json={"content": summary_message},
)

if response.status_code == 204:
    print("Message sent to Discord successfully.")
else:
    print(f"Failed to send message: {response.status_code} - {response.text}")
    sys.exit(1)
