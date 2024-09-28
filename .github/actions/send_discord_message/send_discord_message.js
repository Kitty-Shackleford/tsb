const core = require('@actions/core');
const axios = require('axios');

async function run() {
    try {
        const summary = core.getInput('summary') || 'No summary provided.';  // Default message if summary is empty
        const webhookUrl = process.env.DISCORD_WEBHOOK;

        if (!webhookUrl) {
            throw new Error('DISCORD_WEBHOOK is not set.');
        }

        const response = await axios.post(webhookUrl, {
            content: summary
        });

        if (response.status !== 204) {
            throw new Error(`Failed to send message: ${response.status} - ${response.data}`);
        }

        console.log('Message sent successfully!');
    } catch (error) {
        core.setFailed(error.message);
        // Send the error message to Discord as well
        const webhookUrl = process.env.DISCORD_WEBHOOK;
        if (webhookUrl) {
            await axios.post(webhookUrl, {
                content: `Error occurred: ${error.message}`
            });
        }
    }
}

run();
