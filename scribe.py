import os
import requests
import xml.etree.ElementTree as ET
import random

def fetch_quote_from_kanye():
    """Fetch a quote from the Kanye West API."""
    try:
        response = requests.get("https://api.kanye.rest/")
        response.raise_for_status()
        return response.json().get('quote', 'Kanye quote unavailable')
    except Exception as e:
        print(f"Error fetching quote from Kanye API: {e}")
        return "Kanye quote unavailable"

def fetch_quote_from_api_ninja(category=None):
    """Fetch a quote from API Ninja."""
    try:
        url = "https://api.api-ninjas.com/v1/quotes"
        headers = {'X-Api-Key': os.getenv('API_NINJA_KEY')}
        params = {}
        if category:
            params['category'] = category
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()[0].get('quote', 'Ninja quote unavailable')
    except Exception as e:
        print(f"Error fetching quote from API Ninja: {e}")
        return "Ninja quote unavailable"

def create_messages_xml():
    """Create a new messages.xml file with server messages."""
    root = ET.Element("messages")

    # Static header messages with properties
    static_headers = [
        {
            "deadline": 120,
            "shutdown": 1,
            "text": "[TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB]  [ SERVER: TSB | https://discord.gg/jvDrNT6aCx ]  WILL REBOOT IN #tmin MINS PARK AND EXIT YOUR VEHICLE |  https://shop.killfeed.xyx | [TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB]"
        },
        {
            "delay": 1,
            "onConnect": 1,
            "text": "[TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB] | YOU ARE RIDING THE SHORT BUS | JOIN THE DISCORD | https://discord.gg/jvDrNT6aCx | YOU ARE RIDING THE SHORT BUS | [TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB]"
        },
        {
            "repeat": 6,
            "text": "[TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB TSB] | LEADERBOARD | https://player.killfeed.xyz/dashboard/global/statistics/ | SHOP | https://shop.killfeed.xyx | JOIN THE DISCORD | https://discord.gg/jvDrNT6aCx | [TSB TSB TSB TSB TSB TSB TSB TSB TSB]"
        }
    ]

    # Fetch dynamic messages from the APIs
    dynamic_quotes = [
        fetch_quote_from_kanye(),
        fetch_quote_from_api_ninja(category=random.choice(['inspirational', 'funny', 'love', 'life', 'success'])),
        fetch_quote_from_api_ninja(category=random.choice(['motivational', 'friendship', 'happiness', 'freedom', 'courage'])),
        fetch_quote_from_api_ninja(category=random.choice(['family', 'knowledge', 'business', 'art', 'dreams']))
    ]

    # Staggered repeat intervals in minutes for messages
    stagger_intervals = [120, 119, 118, 117]

    # Add messages to XML with staggered intervals
    all_messages = static_headers + [
        {"repeat": stagger_time, "text": f"[{quote}]"} 
        for stagger_time, quote in zip(stagger_intervals[1:], dynamic_quotes)
    ]

    # Add static headers to XML
    for header in all_messages:
        message_element = ET.SubElement(root, "message")
        if "deadline" in header:
            ET.SubElement(message_element, "deadline").text = str(header["deadline"])
        if "shutdown" in header:
            ET.SubElement(message_element, "shutdown").text = str(header["shutdown"])
        if "delay" in header:
            ET.SubElement(message_element, "delay").text = str(header["delay"])
        if "onConnect" in header:
            ET.SubElement(message_element, "onconnect").text = str(header["onConnect"])
        if "repeat" in header:
            ET.SubElement(message_element, "repeat").text = str(header["repeat"])
        text_element = ET.SubElement(message_element, "text")
        text_element.text = header["text"]

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
