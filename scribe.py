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

def fetch_random_message():
    """Fetch a random quote from multiple APIs."""
    api_endpoints = [
        "https://api.quotable.io/random",
        "http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en",
        "https://quotes.rest/qod",
        "https://zenquotes.io/api/random"
    ]

    for endpoint in api_endpoints:
        try:
            response = requests.get(endpoint)
            response.raise_for_status()

            if endpoint == "https://api.quotable.io/random":
                quote_data = response.json()
                quote = quote_data['content']
                if len(quote.split()) < 10:
                    return f"{quote} — {quote_data['author']}"
            
            elif endpoint == "http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en":
                quote_data = response.json()
                quote = quote_data['quoteText']
                if len(quote.split()) < 10:
                    return f"{quote} — {quote_data['quoteAuthor']}"
            
            elif endpoint == "https://quotes.rest/qod":
                quote_data = response.json()
                quote = quote_data['contents']['quotes'][0]['quote']
                if len(quote.split()) < 10:
                    return f"{quote} — {quote_data['contents']['quotes'][0]['author']}"
            
            elif endpoint == "https://zenquotes.io/api/random":
                quote_data = response.json()
                quote = quote_data[0]['q']
                if len(quote.split()) < 10:
                    return f"{quote} — {quote_data[0]['a']}"

        except Exception as e:
            print(f"Error fetching quote from {endpoint}: {e}")

    return "Stay inspired!"  # Fallback message

def modify_messages_xml(file_path):
    """Modify the messages.xml file."""
    # Download the existing XML file
    download_file_via_ftp(file_path, 'messages.xml')

    # Parse and modify the XML file
    tree = ET.parse('messages.xml')
    root = tree.getroot()

    # Change text within brackets for each message
    for message in root.findall('message'):
        text_element = message.find('text')
        if text_element is not None:
            # Fetch a new random quote
            new_quote = fetch_random_message()
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
