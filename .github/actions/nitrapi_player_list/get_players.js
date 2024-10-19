const core = require('@actions/core');
const axios = require('axios');

async function run() {
    try {
        const nitradoId = core.getInput('nitrado_id');
        const nitradoToken = core.getInput('nitrado_token');
        const discordWebhook = core.getInput('discord_webhook');

        // Fetch players from the Nitrado API
        const response = await axios.get(`https://api.nitrado.net/services/${nitrado_id}/gameservers/games/players`, {
            headers: {
                'Authorization': `Bearer ${nitradoToken}`,
                'Accept': 'application/json',
            }
        });

        const players = response.data.data.players; // Access the players array
        let message = 'Player List:\n';

        // Check if players array is empty
        if (players.length === 0) {
            message += 'No players currently online.';
        } else {
            players.forEach(player => {
                message += `- ${player.name} (ID: ${player.id})\n`;
            });
        }

        // Send the message to Discord
        await axios.post(discordWebhook, { content: message });

        console.log('Player list sent to Discord successfully!');
    } catch (error) {
        core.setFailed(`Error: ${error.message}`);
        // Send error message to Discord if the webhook is provided
        if (discordWebhook) {
            await axios.post(discordWebhook, { content: `Error: ${error.message}` });
        }
    }
}

run();

