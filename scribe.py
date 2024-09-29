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
            # Directly set the new quote as the text
            text_element.text = new_quote

    # Save the modified XML back to file
    tree.write('messages.xml')

    # Upload the modified XML back to the server
    upload_file_via_ftp('messages.xml', file_path)

    # Clean up the temporary local file
    os.remove('messages.xml')
