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

def upload_file_via_ftp(local_path, remote_path):
    """Upload a file to the FTP server."""
    with FTP(FTP_HOST) as ftp:
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        with open(local_path, 'rb') as local_file:
            ftp.storbinary(f'STOR {remote_path}', local_file)

def fetch_quotes_from_api():
    """Fetch quotes from an external API."""
    quotes = []
    try:
        response = requests.get("https://api.quotable.io/quotes?limit=4")
        response.raise_for_status()
        data = response.json()

        for quote in data['results']:
            quotes.append((quote['content'], quote['author']))  # Add quote and author
    except Exception as e:
        print(f"Error fetching quotes: {e}")

    return quotes

def create_messages_xml():
    """Create a new messages.xml file with server messages."""
    root = ET.Element("messages")

    # Static header messages (kept unchanged for TV centering)
    static_headers = [
        {
            "text": "[TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB] [ SERVER: TSB | https://discord.gg/jvDrNT6aCx ]  WILL REBOOT IN #tmin MINS PARK AND EXIT YOUR VEHICLE |  https://shop.killfeed.xyx | [TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB]"
        },
        {
            "text": "[TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB] | YOU ARE RIDING THE SHORT BUS | JOIN THE DISCORD | https://discord.gg/jvDrNT6aCx | YOU ARE RIDING THE SHORT BUS | [TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB]"
        },
        {
            "text": "[TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB] | LEADERBOARD | https://player.killfeed.xyz/dashboard/global/statistics/ | SHOP | https://shop.killfeed.xyx | JOIN THE DISCORD | https://discord.gg/jvDrNT6aCx | [TSB TSB TSB TSB TSB TSB TSB TSB TSB]"
        }
    ]

    # Fetch dynamic messages from an external API
    dynamic_quotes = fetch_quotes_from_api()

    # Add static headers to XML
    for header in static_headers:
        message_element = ET.SubElement(root, "message")
        text_element = ET.SubElement(message_element, "text")
        text_element.text = header["text"]

    # Add dynamic messages to XML
    for repeat_count, (quote, author) in zip([90, 69, 33, 13], dynamic_quotes):
        message_element = ET.SubElement(root, "message")
        ET.SubElement(message_element, "repeat").text = str(repeat_count)
        text_element = ET.SubElement(message_element, "text")
        text_element.text = f"[{quote} — {author}]"

    # Write to a new XML file
    tree = ET.ElementTree(root)
    tree.write('messages.xml', encoding='utf-8', xml_declaration=True)

def upload_new_messages_file(file_path):
    """Upload the new messages.xml file to the FTP server."""
    upload_file_via_ftp(file_path, '/dayzxb_missions/dayzOffline.enoch/custom/messages.xml')

if __name__ == "__main__":
    create_messages_xml()
    upload_new_messages_file('messages.xml')
    print("Successfully created and uploaded messages.xml.")

