const core = require('@actions/core');
const axios = require('axios');

async function run() {
    try {
        const summary = core.getInput('summary');
        const webhookUrl = process.env.DISCORD_WEBHOOK;

        if (!webhookUrl) {
            throw new Error('DISCORD_WEBHOOK is not set.');
        }

        const message = summary || 'No summary provided.';
        const response = await axios.post(webhookUrl, {
            content: message
        });

        if (response.status !== 204) {
            throw new Error(`Failed to send message: ${response.status} - ${response.data}`);
        }

        console.log('Message sent successfully!');
    } catch (error) {
        core.setFailed(error.message);
        // Send the error message to Discord as well
        try {
            await axios.post(webhookUrl, {
                content: `Error: ${error.message}`
            });
        } catch (sendError) {
            console.error(`Failed to send error message to Discord: ${sendError.message}`);
        }
    }
}

run();
