def generate_markdown(services, api_key):
    """Generate enhanced Markdown output for the gameserver details."""
    markdown_output = "# 🎮 **Gameserver Details**\n\n"
    markdown_output += "Here are the details for your gameservers hosted on Nitrado. Enjoy the game! 🎉\n\n"

    for service in services:
        service_id = service.get("id")
        gameserver = fetch_gameserver_details(service_id, api_key)

        if gameserver:
            server_name = format_server_name(gameserver)
            markdown_output += f"## 🖥️ **{server_name}**\n\n"

            markdown_output += "| **Property**         | **Value**                   |\n"
            markdown_output += "|----------------------|------------------------------|\n"

            player_count = gameserver.get("query", {}).get("player_current", 0)
            max_slots = gameserver.get("slots", 0)

            properties = {
                "Status": get_status_message(gameserver.get('status', 'Unknown')),
                "Player Count": f"👥 **{player_count}/{max_slots}**",
                "Last Update": f"🕒 **{gameserver.get('game_specific', {}).get('last_update', 'None')}**",
                "Comment": f"💬 **{service.get('comment', 'None')}**",
                "Banned Users": f"🚫 **{', '.join(gameserver.get('general', {}).get('bans', '').splitlines() or ['None'])}**",
                "Game": f"🎮 **{gameserver.get('game_human', 'Unknown')}**",
                "Mission": f"🏆 **{gameserver.get('settings', {}).get('config', {}).get('mission', 'Unknown')}**",
                "3rd Person": "✅ **Enabled**" if gameserver.get("settings", {}).get("config", {}).get("disable3rdPerson", "1") == "0" else "❌ **Disabled**",
                "Crosshair": "✅ **Enabled**" if gameserver.get("settings", {}).get("config", {}).get("disableCrosshair", "1") == "0" else "❌ **Disabled**",
                "Shot Validation": "✅ **Enabled**" if gameserver.get("settings", {}).get("config", {}).get("shotValidation", "0") == "1" else "❌ **Disabled**",
                "Mouse and Keyboard": "✅ **Enabled**" if gameserver.get("settings", {}).get("config", {}).get("enableMouseAndKeyboard", "1") == "1" else "❌ **Disabled**",
                "Whitelist": "✅ **Enabled**" if gameserver.get("settings", {}).get("config", {}).get("enableWhitelist", "1") == "1" else "❌ **Disabled**",
                "Base Damage": "✅ **Enabled**" if gameserver.get("settings", {}).get("config", {}).get("disableBaseDamage", "1") == "0" else "❌ **Disabled**",
                "Container Damage": "✅ **Enabled**" if gameserver.get("settings", {}).get("config", {}).get("disableContainerDamage", "1") == "0" else "❌ **Disabled**",
                "Priority": f"🔝 **{gameserver.get('settings', {}).get('general', {}).get('priority', 'None').replace('\n', ', ')}**",
                "Whitelist": f"📜 **{gameserver.get('settings', {}).get('general', {}).get('whitelist', 'None').replace('\n', ', ')}**",
                "Version": f"📅 **{gameserver.get('query', {}).get('version', 'Unknown')}**",
            }

            for key, value in properties.items():
                markdown_output += f"| {key} | {value} |\n"

            markdown_output += "\n---\n\n"
        else:
            logging.warning(f"No gameserver details found for service ID {service_id}.")

    return markdown_output
