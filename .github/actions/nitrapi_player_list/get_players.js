const core = require('@actions/core');
const axios = require('axios');

async function run() {
    try {
        const nitradoId = core.getInput('nitrado_id');
        const nitradoToken = core.getInput('nitrado_token');
        const discordWebhook = core.getInput('discord_webhook');

        // Fetch players from the Nitrado API
        const response = await axios.get(`https://api.nitrado.net/services/${nitradoId}/gameservers/games/players`, {
            headers: {
                'Authorization': `Bearer ${nitradoToken}`,
                'Accept': 'application/json',
            }
        });

        const players = response.data.data;

        // Create a message for Discord
        let message = 'Player List:\n';
        players.forEach(player => {
            message += `- ${player.name} (ID: ${player.id})\n`;
        });

        // Send the message to Discord
        await axios.post(discordWebhook, { content: message });

        console.log('Player list sent to Discord successfully!');
    } catch (error) {
        core.setFailed(`Error: ${error.message}`);
        // Optionally, send error message to Discord if needed
        if (discordWebhook) {
            await axios.post(discordWebhook, { content: `Error: ${error.message}` });
        }
    }
}

run();
