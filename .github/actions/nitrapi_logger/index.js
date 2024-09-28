import fs from 'fs';
import path from 'path';
import fetch from 'node-fetch';
import * as core from '@actions/core';
import * as github from '@actions/github';

async function run() {
    try {
        const { owner, repo } = github.context.repo;
        const workflowRunId = github.context.runId;

        // Fetch the workflow run logs
        const response = await fetch(`https://api.github.com/repos/${owner}/${repo}/actions/runs/${workflowRunId}/logs`, {
            headers: {
                'Authorization': `token ${process.env.GITHUB_TOKEN}`,
                'Accept': 'application/vnd.github.v3+json'
            }
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch logs: ${response.statusText}`);
        }

        const logUrl = response.url; // URL to download the log file

        // Download the log file
        const logResponse = await fetch(logUrl);
        const logFilePath = path.join(process.cwd(), 'recent_log.txt');
        const logStream = fs.createWriteStream(logFilePath);

        logResponse.body.pipe(logStream);

        logStream.on('finish', () => {
            core.setOutput('log-file', logFilePath);
            console.log(`Log file downloaded: ${logFilePath}`);
        });
    } catch (error) {
        core.setFailed(error.message);
    }
}

run();

