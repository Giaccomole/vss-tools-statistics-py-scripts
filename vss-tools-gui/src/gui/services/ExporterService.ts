import { exec } from 'child_process';
import { promisify } from 'util';
import * as fs from 'fs';
import * as path from 'path';

const execAsync = promisify(exec);

export class ExporterService {
    private exporters: string[] = [];
    private vssToolsPath: string;

    constructor() {
        this.fetchAvailableExporters();
        // Path to the main VSS tools directory
        this.vssToolsPath = path.resolve(__dirname, '../../../..'); // Should point to vss-tools root
    }

    private fetchAvailableExporters(): void {
        // Available exporters from the CLI
        this.exporters = [
            "apigear",
            "binary",
            "csv",
            "ddsidl",
            "franca",
            "plantuml",
            "graphql",
            "id",
            "json",
            "jsonschema",
            "protobuf",
            "yaml",
            "tree",
            "samm",
            "go",
        ];
    }

    public getExporters(): string[] {
        return this.exporters;
    }

    public async generateFile(path: string, exporter: string): Promise<string> {
        if (!path || !exporter) {
            return 'Please select a file path and exporter';
        }

        // Check if the file exists
        if (!fs.existsSync(path)) {
            return `Error: File not found at path: ${path}\n\nPlease enter a valid path to a .vspec file.`;
        }

        try {
            // Create a temporary output file
            const outputDir = '/tmp/vss-tools-gui-output';
            if (!fs.existsSync(outputDir)) {
                fs.mkdirSync(outputDir, { recursive: true });
            }
            
            const outputFile = `${outputDir}/output.${this.getFileExtension(exporter)}`;
            
            // Build the command to run VSS tools
            const command = `cd ${this.vssToolsPath} && python -m vss_tools export ${exporter} --vspec "${path}" --output "${outputFile}"`;
            
            console.log(`Executing command: ${command}`);
            
            // Execute the command
            const { stdout, stderr } = await execAsync(command);
            
            if (stderr && !stderr.includes('WARNING')) {
                return `Error executing exporter:\n${stderr}`;
            }
            
            // Read the generated file
            if (fs.existsSync(outputFile)) {
                const content = fs.readFileSync(outputFile, 'utf8');
                
                // Clean up the temp file
                fs.unlinkSync(outputFile);
                
                return `Generated using ${exporter} exporter:\n\n${content}`;
            } else {
                return `Exporter completed but no output file was generated.\nCommand output:\n${stdout}`;
            }
            
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            return `Error generating file with ${exporter} exporter:\n${errorMessage}\n\nMake sure VSS tools are properly installed and the file path is correct.`;
        }
    }

    private getFileExtension(exporter: string): string {
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
    }
}