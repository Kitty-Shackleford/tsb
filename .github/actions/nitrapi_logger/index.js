import fs from 'fs';
import path from 'path';
import fetch from 'node-fetch';
import * as core from '@actions/core';
import * as github from '@actions/github';

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
        throw new Error(`Failed to fetch file list: ${response.statusText}`);
    }

    return response.json();
}

async function downloadLogFile(logPath) {
    const response = await fetch(`https://api.nitrado.net/services/${NITRADO_ID}/gameservers/file_server/download?file=/games/${NITRADO_ID}/noftp/${logPath}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${API_TOKEN}`
        }
    });

    if (!response.ok) {
        throw new Error(`Failed to download log file: ${response.statusText}`);
    }

    const logFilePath = path.join(process.cwd(), 'recent_log.txt');
    const logStream = fs.createWriteStream(logFilePath);
    response.body.pipe(logStream);

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

        // Determine the log path based on the game type
        let logPath = '';
        if (GAME_TYPE === 'dayzps') {
            logPath = 'dayzps/config/DayZServer_PS4_x64.ADM';
        } else if (GAME_TYPE === 'dayzxb') {
            logPath = 'dayzxb/config/DayZServer_X1_x64.ADM';
        } else {
            core.setFailed('This action only supports: DayZ PS4 and DayZ Xbox');
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


