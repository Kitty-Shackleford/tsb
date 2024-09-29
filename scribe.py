import os
import requests
from ftplib import FTP
import xml.etree.ElementTree as ET

# Ensure the FTP credentials are set
FTP_HOST = os.getenv("FTP_SERVER")
FTP_USER = os.getenv("FTP_USERNAME")
FTP_PASS = os.getenv("FTP_PASSWORD")
if not all([FTP_HOST, FTP_USER, FTP_PASS]):
    print("Error: FTP credentials are not set.")
    exit(1)

# Count of messages from the bottom up to modify
MESSAGES_COUNTER = 4 

def download_file_via_ftp(remote_path, local_path):
    """Download a file from the FTP server."""
    with FTP(FTP_HOST) as ftp:
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        with open(local_path, 'wb') as local_file:
            ftp.retrbinary(f'RETR {remote_path}', local_file.write)

def upload_file_via_ftp(local_path, remote_path):
    """Upload a file to the FTP server."""
    with FTP(FTP_HOST) as ftp:
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        with open(local_path, 'rb') as local_file:
            ftp.storbinary(f'STOR {remote_path}', local_file)

def fetch_random_quote():
    """Fetch a random quote from an online API that is under 10 words."""
    for _ in range(5):  # Try up to 5 times
        try:
            response = requests.get("https://api.quotable.io/random")
            response.raise_for_status()
            quote_data = response.json()
            quote = quote_data['content']
            if len(quote.split()) < 10:
                return f"{quote} — {quote_data['author']}"
        except Exception as e:
            print(f"Error fetching quote: {e}")
    return "Stay inspired!"  # Fallback quote

def modify_messages_xml(file_path):
    """Modify the messages.xml file."""
    # Download the existing XML file
    download_file_via_ftp(file_path, 'messages.xml')

    # Parse and modify the XML file
    tree = ET.parse('messages.xml')
    root = tree.getroot()

    # Get all messages
    messages = root.findall('message')

    # Determine how many messages to modify based on MESSAGES_COUNTER
    num_messages_to_modify = min(MESSAGES_COUNTER, len(messages))  # Modify up to the last `MESSAGES_COUNTER` messages

    # Modify only the last `num_messages_to_modify` messages
    for message in messages[-num_messages_to_modify:]:  # Last `num_messages_to_modify` messages
        text_element = message.find('text')
        if text_element is not None:
            # Fetch a new random quote
            new_quote = fetch_random_quote()
            # Replace content in brackets with the new quote
            original_text = text_element.text
            start_index = original_text.find('[')
            end_index = original_text.find(']') + 1
            updated_text = original_text[:start_index] + new_quote + original_text[end_index:]
            text_element.text = updated_text

    # Save the modified XML back to file
    tree.write('messages.xml')

    # Upload the modified XML back to the server
    upload_file_via_ftp('messages.xml', file_path)

    # Clean up the temporary local file
    os.remove('messages.xml')

if __name__ == "__main__":
    xml_file_path = '/dayzxb_missions/dayzOffline.enoch/custom/messages.xml'
    modify_messages_xml(xml_file_path)
    print("Successfully modified and uploaded messages.xml.")
