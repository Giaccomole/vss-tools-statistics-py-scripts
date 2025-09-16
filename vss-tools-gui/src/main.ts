import express from 'express';
import path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs';

const execAsync = promisify(exec);

console.log('Starting VSS Tools GUI server...');

const app = express();
const port = 3000;

// Path to the main VSS tools directory
const vssToolsPath = '/Users/q674786/Desktop/vss-tools';

// File extension mapping for different exporters
const getFileExtension = (exporter: string): string => {
    const extensions: { [key: string]: string } = {
        'json': 'json',
        'yaml': 'yaml', 
        'csv': 'csv',
        'tree': 'txt',
        'graphql': 'graphql',
        'protobuf': 'proto',
        'binary': 'bin',
        'id': 'txt',
        'jsonschema': 'json',
        'ddsidl': 'idl',
        'franca': 'fidl',
        'apigear': 'json',
        'plantuml': 'puml',
        'samm': 'ttl',
        'go': 'go'
    };
    return extensions[exporter] || 'txt';
};

// Middleware to parse JSON
app.use(express.json());

// Serve static files from public directory
app.use(express.static(path.join(__dirname, '../public')));

// API endpoint for export
app.post('/api/export', async (req, res) => {
    const { path: filePath, exporter } = req.body;
    
    console.log(`API call: ${exporter} for ${filePath}`);
    
    if (!filePath || !exporter) {
        return res.send('Please select a file path and exporter');
    }

    // Check if the file exists
    if (!fs.existsSync(filePath)) {
        return res.send(`Error: File not found at path: ${filePath}\n\nPlease enter a valid path to a .vspec file.`);
    }

    try {
        // Create a temporary output file
        const outputDir = '/tmp/vss-tools-gui-output';
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }
        
        const outputFile = `${outputDir}/output.${getFileExtension(exporter)}`;
        
        // Build the command to run VSS tools using the virtual environment
        // We need to stay in the vss-tools directory to source the venv
        const command = `cd ${vssToolsPath} && source .venv/bin/activate && vspec export ${exporter} --vspec "${filePath}" --output "${outputFile}"`;
        
        console.log(`Executing command: ${command}`);
        
        // Execute the command
        const { stdout, stderr } = await execAsync(command);
        
        if (stderr && !stderr.includes('WARNING')) {
            return res.send(`Error executing exporter:\n${stderr}`);
        }
        
        // Read the generated file
        if (fs.existsSync(outputFile)) {
            const content = fs.readFileSync(outputFile, 'utf8');
            
            // Clean up the temp file
            fs.unlinkSync(outputFile);
            
            return res.send(content);
        } else {
            return res.send(`Exporter completed but no output file was generated.\nCommand output:\n${stdout}`);
        }
        
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        console.error('API error:', errorMessage);
        return res.send(`Error generating file with ${exporter} exporter:\n${errorMessage}\n\nMake sure VSS tools are properly installed and the file path is correct.`);
    }
});

// API endpoint for downloading files
app.post('/api/download', async (req, res) => {
    const { path: filePath, exporter } = req.body;
    
    console.log(`Download request: ${exporter} for ${filePath}`);
    
    if (!filePath || !exporter) {
        return res.status(400).send('Please select a file path and exporter');
    }

    // Check if the file exists
    if (!fs.existsSync(filePath)) {
        return res.status(404).send(`File not found at path: ${filePath}`);
    }

    try {
        // Create a temporary output file
        const outputDir = '/tmp/vss-tools-gui-output';
        if (!fs.existsSync(outputDir)) {
            fs.mkdirSync(outputDir, { recursive: true });
        }
        
        const outputFile = `${outputDir}/download_${Date.now()}.${getFileExtension(exporter)}`;
        
        // Build the command to run VSS tools
        const command = `cd ${vssToolsPath} && source .venv/bin/activate && vspec export ${exporter} --vspec "${filePath}" --output "${outputFile}"`;
        
        console.log(`Executing download command: ${command}`);
        
        // Execute the command
        const { stdout, stderr } = await execAsync(command);
        
        if (stderr && !stderr.includes('WARNING')) {
            console.error('Download error:', stderr);
            return res.status(500).send(`Error executing exporter: ${stderr}`);
        }
        
        // Send the generated file
        if (fs.existsSync(outputFile)) {
            const filename = `vss_export.${getFileExtension(exporter)}`;
            
            res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
            res.setHeader('Content-Type', 'application/octet-stream');
            
            // Send file and clean up
            res.sendFile(outputFile, (err) => {
                if (err) {
                    console.error('Error sending file:', err);
                } else {
                    console.log(`File downloaded: ${filename}`);
                }
                // Clean up the temp file
                if (fs.existsSync(outputFile)) {
                    fs.unlinkSync(outputFile);
                }
            });
        } else {
            return res.status(500).send(`Exporter completed but no output file was generated.`);
        }
        
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        console.error('Download API error:', errorMessage);
        return res.status(500).send(`Error generating file: ${errorMessage}`);
    }
});

// Serve the main HTML file for the root route
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../public/index.html'));
});

app.listen(port, () => {
    console.log(`VSS Tools GUI server running at http://localhost:${port}`);
});
