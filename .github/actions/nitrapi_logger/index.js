import fs from 'fs';
import path from 'path';
import fetch from 'node-fetch';
import * as core from '@actions/core';

const NITRADO_ID = core.getInput('nitrado_id');
const API_TOKEN = core.getInput('token');
const GAME_TYPE = core.getInput('game');

async function getFileList() {
    const response = await fetch(`https://api.nitrado.net/services/${NITRADO_ID}/gameservers/file_server/list`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${API_TOKEN}`,
            'Content-Type': 'application/json'
        }
    });

    if (!response.ok) {
        const errorMessage = await response.text();
        throw new Error(`Failed to fetch file list: ${response.statusText} - ${errorMessage}`);
    }

    const data = await response.json();
    return data.data.entries; // Return the entries from the response
}

async function downloadLogFile(logPath) {
    const response = await fetch(`https://api.nitrado.net/services/${NITRADO_ID}/gameservers/file_server/download?file=/games/${logPath}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${API_TOKEN}`
        }
    });

    if (!response.ok) {
        throw new Error(`Failed to initiate download log file: ${response.statusText}`);
    }

    const downloadData = await response.json();

    // Check if the response contains a valid download URL
    if (downloadData.status !== "success" || !downloadData.data.token) {
        throw new Error('Failed to retrieve download token.');
    }

    const downloadUrl = downloadData.data.token.url;

    // Proceed to download the log file using the token URL
    const logResponse = await fetch(downloadUrl);
    
    if (!logResponse.ok) {
        throw new Error(`Failed to download log file from URL: ${logResponse.statusText}`);
    }

    const logFilePath = path.join(process.cwd(), 'recent_log.txt');
    const logStream = fs.createWriteStream(logFilePath);
    logResponse.body.pipe(logStream);

    return new Promise((resolve, reject) => {
        logStream.on('finish', () => {
            console.log(`Log file downloaded: ${logFilePath}`);
            resolve(logFilePath);
        });
        logStream.on('error', (err) => {
            reject(new Error(`Error writing log file: ${err.message}`));
        });
    });
}

async function run() {
    try {
        const fileList = await getFileList();

        // Determine the log path and extract the username
        let logPath = '';
        let username = '';

        if (GAME_TYPE === 'dayzps') {
            logPath = 'dayzps/config/DayZServer_PS4_x64.ADM';
            username = fileList.find(entry => entry.path.includes('/games/') && entry.type === 'dir')?.owner; // Extract username from the directory
        } else if (GAME_TYPE === 'dayzxb') {
            logPath = 'dayzxb/config/DayZServer_X1_x64.ADM';
            username = fileList.find(entry => entry.path.includes('/games/') && entry.type === 'dir')?.owner; // Extract username from the directory
        } else {
            core.setFailed('This action only supports: DayZ PS4 and DayZ Xbox');
            return;
        }

        if (!username) {
            core.setFailed('Username not found for the specified game type.');
            return;
        }

        // Download the log file
        const downloadedLogFilePath = await downloadLogFile(logPath);
        core.setOutput('log-file', downloadedLogFilePath);
    } catch (error) {
        core.setFailed(error.message);
    }
}

// Run the action
run();
