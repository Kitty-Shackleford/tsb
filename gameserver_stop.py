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

# Prepare Markdown output
markdown_output = "# Stop Nitrado Gameserver\n\n"

# Make the POST request to stop the gameserver
response = requests.post(
    f'https://api.nitrado.net/services/{NITRADO_ID}/gameservers/stop',
    headers={'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'},
    json=stop_params
)

if response.ok:
    markdown_output += "### Success:\n"
    markdown_output += f"- Status: **{response.json().get('status')}**\n"
    markdown_output += f"- Message: **{response.json().get('message')}**\n"
else:
    markdown_output += "### Error:\n"
    markdown_output += f"- Status Code: **{response.status_code}**\n"
    markdown_output += f"- Message: **{response.text}**\n"

# Write output to a Markdown file
try:
    with open("output.md", "w") as f:
        f.write(markdown_output)
    print("Output successfully written to output.md")
except Exception as e:
    print(f"Error writing to output.md: {e}")

# Debug: Print the output for verification
print("Markdown output:\n", markdown_output)

