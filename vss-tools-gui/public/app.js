class NotificationManager {
    static show(message, type = 'info') {
        const notification = document.getElementById('notification');
        const messageElement = document.getElementById('notification-message');
        
        // Set message and type
        messageElement.textContent = message;
        notification.className = `notification is-${type} mb-5`;
        
        // Show notification
        notification.classList.remove('is-hidden');
        
        // Auto-hide after 5 seconds for success/info, keep error/warning visible
        if (type === 'success' || type === 'info') {
            setTimeout(() => {
                this.hide();
            }, 5000);
        }
    }
    
    static hide() {
        const notification = document.getElementById('notification');
        notification.classList.add('is-hidden');
    }
}

class ProgressManager {
    static show(text = 'Processing...') {
        const container = document.getElementById('progress-container');
        const textElement = document.getElementById('progress-text');
        const progressBar = document.getElementById('progress-bar');
        
        textElement.textContent = text;
        progressBar.value = 0;
        container.classList.remove('is-hidden');
    }
    
    static update(value, text) {
        const progressBar = document.getElementById('progress-bar');
        const textElement = document.getElementById('progress-text');
        
        progressBar.value = value;
        if (text) textElement.textContent = text;
    }
    
    static hide() {
        const container = document.getElementById('progress-container');
        container.classList.add('is-hidden');
    }
}

class ValidationManager {
    static validatePath(path) {
        const pathInput = document.getElementById('path-input');
        const validIcon = document.getElementById('path-valid-icon');
        const invalidIcon = document.getElementById('path-invalid-icon');
        
        // Basic validation
        const isValid = path.trim().length > 0 && path.includes('.vspec');
        
        if (isValid) {
            pathInput.classList.remove('is-danger');
            pathInput.classList.add('is-success');
            validIcon.classList.remove('is-hidden');
            invalidIcon.classList.add('is-hidden');
        } else if (path.trim().length > 0) {
            pathInput.classList.remove('is-success');
            pathInput.classList.add('is-danger');
            validIcon.classList.add('is-hidden');
            invalidIcon.classList.remove('is-hidden');
        } else {
            pathInput.classList.remove('is-success', 'is-danger');
            validIcon.classList.add('is-hidden');
            invalidIcon.classList.add('is-hidden');
        }
        
        return isValid;
    }
}

class PreviewManager {
    static init() {
        const toggleBtn = document.getElementById('preview-toggle');
        const previewContent = document.getElementById('preview-content');
        const icon = toggleBtn.querySelector('i');
        
        toggleBtn.addEventListener('click', () => {
            const isCollapsed = previewContent.classList.contains('is-hidden');
            
            if (isCollapsed) {
                previewContent.classList.remove('is-hidden');
                icon.className = 'fas fa-angle-up';
            } else {
                previewContent.classList.add('is-hidden');
                icon.className = 'fas fa-angle-down';
            }
        });
    }
    
    static showEmpty() {
        const preview = document.getElementById('preview');
        preview.innerHTML = `
            <div class="has-text-centered py-6">
                <span class="icon is-large has-text-grey">
                    <i class="fas fa-file-import fa-2x"></i>
                </span>
                <p class="has-text-grey-light mt-3">
                    Select a file path and exporter to generate a preview
                </p>
                <p class="has-text-grey" style="font-size: 0.85rem;">
                    Click "Generate Preview" to see the exported content with syntax highlighting
                </p>
            </div>
        `;
    }
    
    static showLoading() {
        const preview = document.getElementById('preview');
        preview.innerHTML = `
            <div class="has-text-centered py-6">
                <div class="skeleton" style="height: 200px; border-radius: 6px;"></div>
                <p class="has-text-grey mt-3">
                    <i class="fas fa-cog fa-spin mr-2"></i>
                    Processing and applying syntax highlighting...
                </p>
            </div>
        `;
    }
    
    static getLanguageFromExporter(exporter) {
        const languageMap = {
            'json': 'json',
            'yaml': 'yaml',
            'csv': 'csv',
            'tree': 'none',
            'jsonschema': 'json',
            'graphql': 'graphql',
            'protobuf': 'protobuf',
            'ddsidl': 'cpp', // IDL is similar to C++
            'go': 'go',
            'franca': 'javascript', // Franca IDL has JS-like syntax
            'binary': 'none',
            'id': 'none',
            'apigear': 'json',
            'plantuml': 'none',
            'samm': 'turtle', // RDF Turtle
            'ttl': 'turtle'
        };
        return languageMap[exporter] || 'none';
    }
    
    static performBasicLinting(content, exporter) {
        const issues = [];
        const lines = content.split('\n').filter(line => line.trim()); // Filter out empty lines
        
        if (!content || content.trim().length === 0) {
            return issues;
        }
        
        switch(exporter) {
            case 'json':
            case 'jsonschema':
            case 'apigear':
                try {
                    JSON.parse(content);
                } catch (e) {
                    issues.push({
                        line: this.getErrorLine(e.message),
                        type: 'error',
                        message: `JSON Syntax Error: ${e.message}`
                    });
                }
                break;
                
            case 'yaml':
                // Basic YAML validation
                lines.forEach((line, index) => {
                    if (line.includes('\t')) {
                        issues.push({
                            line: index + 1,
                            type: 'warning',
                            message: 'YAML should use spaces, not tabs for indentation'
                        });
                    }
                    if (line.trim().startsWith('-') && !line.includes(' ')) {
                        issues.push({
                            line: index + 1,
                            type: 'warning',
                            message: 'List items should have a space after the dash'
                        });
                    }
                });
                break;
                
            case 'csv':
                if (lines.length > 0) {
                    // Basic CSV validation
                    const firstLineColumns = lines[0].split(',').length;
                    lines.forEach((line, index) => {
                        if (line.trim()) {
                            const currentColumns = line.split(',').length;
                            if (currentColumns !== firstLineColumns) {
                                issues.push({
                                    line: index + 1,
                                    type: 'warning',
                                    message: `Column count mismatch. Expected ${firstLineColumns} columns, found ${currentColumns}`
                                });
                            }
                        }
                    });
                    
                    // Check for potential issues with quotes
                    lines.forEach((line, index) => {
                        const quoteCount = (line.match(/"/g) || []).length;
                        if (quoteCount % 2 !== 0) {
                            issues.push({
                                line: index + 1,
                                type: 'error',
                                message: 'Unmatched quotes in CSV line'
                            });
                        }
                    });
                }
                break;
                
            case 'go':
                // Basic Go syntax checks
                lines.forEach((line, index) => {
                    if (line.includes('func ') && !line.includes('(') && !line.includes(')')) {
                        issues.push({
                            line: index + 1,
                            type: 'error',
                            message: 'Function declaration missing parentheses'
                        });
                    }
                    if (line.trim().endsWith(';') && !line.includes('for ') && !line.includes('if ')) {
                        issues.push({
                            line: index + 1,
                            type: 'info',
                            message: 'Semicolons are optional in Go'
                        });
                    }
                });
                break;
                
            default:
                // For other formats, just check for basic issues
                if (content.includes('Error:')) {
                    issues.push({
                        line: 1,
                        type: 'error',
                        message: 'Content contains error messages'
                    });
                }
                break;
        }
        
        return issues;
    }
    
    static getErrorLine(errorMessage) {
        const match = errorMessage.match(/line (\d+)/i);
        return match ? parseInt(match[1]) : 1;
    }
    
    static showContent(content, exporter) {
        const preview = document.getElementById('preview');
        const isError = content.startsWith('Error:');
        
        if (isError) {
            preview.innerHTML = `
                <div class="has-text-centered py-6">
                    <span class="icon is-large has-text-danger">
                        <i class="fas fa-exclamation-triangle fa-2x"></i>
                    </span>
                    <p class="has-text-danger mt-3 mb-3">
                        <strong>Generation Failed</strong>
                    </p>
                    <pre style="background-color: #2d1b1b; color: #ff6b6b; padding: 1rem; border-radius: 6px; text-align: left;">${content}</pre>
                </div>
            `;
            return;
        }
        
        // Clean the content - remove any UI text that might have been added
        let cleanContent = content;
        
        // Remove common UI text patterns that might interfere with parsing
        const uiPatterns = [
            /^Generated.*?Content.*?\n/i,
            /^Preview.*?\n/i,
            /^Output.*?\n/i,
            /^\s*[\-=]+\s*\n/,  // Remove separator lines
        ];
        
        uiPatterns.forEach(pattern => {
            cleanContent = cleanContent.replace(pattern, '');
        });
        
        // Trim any leading/trailing whitespace
        cleanContent = cleanContent.trim();
        
        const language = this.getLanguageFromExporter(exporter);
        // Linting is disabled - remove linting logic
        
        // Create the content with syntax highlighting
        let highlightedContent;
        if (language && language !== 'none') {
            // Create a temporary element for Prism processing
            const tempCode = document.createElement('code');
            tempCode.className = `language-${language}`;
            tempCode.textContent = cleanContent;
            
            const tempPre = document.createElement('pre');
            tempPre.className = `language-${language} line-numbers`;
            tempPre.appendChild(tempCode);
            
            // Apply Prism highlighting
            if (window.Prism) {
                Prism.highlightElement(tempCode);
            }
            
            highlightedContent = tempPre.outerHTML;
        } else {
            highlightedContent = `<pre style="margin: 0; white-space: pre-wrap; background-color: #1e1e1e !important; color: #e0e0e0 !important; padding: 1rem; border-radius: 6px; border: 1px solid #4a4a4a; font-family: 'Courier New', monospace;">${cleanContent}</pre>`;
        }
        
        // No linting results - just show the content
        preview.innerHTML = highlightedContent;
        
        // Apply Prism highlighting if it wasn't already applied
        if (window.Prism && language && language !== 'none') {
            Prism.highlightAllUnder(preview);
        }
    }
}

class ExporterService {
    async generateFile(path, exporter) {
        if (!path || !exporter) {
            throw new Error('Please select a file path and exporter');
        }
        
        try {
            const response = await fetch('/api/export', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ path, exporter })
            });
            
            return await response.text();
        } catch (error) {
            throw new Error(`Generation failed: ${error.message}`);
        }
    }

    async downloadFile(path, exporter) {
        if (!path || !exporter) {
            throw new Error('Please select a file path and exporter');
        }
        
        try {
            const response = await fetch('/api/download', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ path, exporter })
            });
            
            if (!response.ok) {
                throw new Error('Download request failed');
            }

            // Get filename from headers
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = `output.${this.getFileExtension(exporter)}`;
            if (contentDisposition) {
                const match = contentDisposition.match(/filename="(.+)"/);
                if (match) filename = match[1];
            }
            
            // Create and trigger download
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            return filename;
        } catch (error) {
            throw error;
        }
    }

    getFileExtension(exporter) {
        const extensions = {
            'json': 'json', 'yaml': 'yaml', 'csv': 'csv', 'tree': 'txt',
            'graphql': 'graphql', 'protobuf': 'proto', 'binary': 'bin',
            'id': 'txt', 'jsonschema': 'json', 'ddsidl': 'idl',
            'franca': 'fidl', 'apigear': 'json', 'plantuml': 'puml',
            'samm': 'ttl', 'go': 'go', 'ttl': 'ttl'
        };
        return extensions[exporter] || 'txt';
    }
}

// Main Application Class
class VSSToolsApp {
    constructor() {
        this.exporterService = new ExporterService();
        this.currentContent = '';
        this.hasValidContent = false;
    }

    init() {
        this.initializeElements();
        this.setupEventListeners();
        this.initializeComponents();
        
        // Show initial empty state
        PreviewManager.showEmpty();
    }

    initializeElements() {
        this.pathInput = document.getElementById('path-input');
        this.exporterSelect = document.getElementById('exporter-select');
        this.generateBtn = document.getElementById('generate-btn');
        this.downloadBtn = document.getElementById('download-btn');
        this.notificationClose = document.getElementById('notification-close');
    }

    initializeComponents() {
        PreviewManager.init();
        
        // Set up notification close handler
        this.notificationClose.addEventListener('click', () => {
            NotificationManager.hide();
        });
    }

    setupEventListeners() {
        // Path input validation
        this.pathInput.addEventListener('input', (e) => {
            ValidationManager.validatePath(e.target.value);
            this.updateButtonStates();
        });

        // Exporter change handler
        this.exporterSelect.addEventListener('change', () => {
            this.updateButtonStates();
        });

        // Generate button
        this.generateBtn.addEventListener('click', () => {
            this.generatePreview();
        });

        // Download button
        this.downloadBtn.addEventListener('click', () => {
            this.downloadFile();
        });
    }

    updateButtonStates() {
        const hasPath = this.pathInput.value.trim().length > 0;
        const hasExporter = this.exporterSelect.value.length > 0;
        const isValid = ValidationManager.validatePath(this.pathInput.value);
        
        this.generateBtn.disabled = !hasPath || !hasExporter || !isValid;
        
        if (this.generateBtn.disabled) {
            this.generateBtn.className = 'button is-info';
        } else {
            this.generateBtn.className = 'button is-info';
        }
    }

    async generatePreview() {
        const path = this.pathInput.value.trim();
        const exporter = this.exporterSelect.value;
        
        if (!path || !exporter) {
            NotificationManager.show('Please fill in all required fields', 'warning');
            return;
        }

        try {
            // Show progress
            ProgressManager.show('Generating preview...');
            PreviewManager.showLoading();
            
            // Simulate progress updates
            ProgressManager.update(30, 'Loading VSSpec file...');
            await new Promise(resolve => setTimeout(resolve, 500));
            
            ProgressManager.update(60, 'Processing with exporter...');
            const content = await this.exporterService.generateFile(path, exporter);
            
            ProgressManager.update(90, 'Formatting output...');
            await new Promise(resolve => setTimeout(resolve, 300));
            
            // Show content
            PreviewManager.showContent(content, exporter);
            this.currentContent = content;
            this.hasValidContent = !content.startsWith('Error:') && content.trim().length > 0;
            
            // Update download button
            this.downloadBtn.disabled = !this.hasValidContent;
            
            if (this.hasValidContent) {
                NotificationManager.show(`Successfully generated ${exporter.toUpperCase()} preview!`, 'success');
                this.downloadBtn.innerHTML = `
                    <span class="icon"><i class="fas fa-download"></i></span>
                    <span>Download ${exporter.toUpperCase()} File</span>
                `;
            } else {
                NotificationManager.show('Generation completed with errors', 'warning');
                this.downloadBtn.innerHTML = `
                    <span class="icon"><i class="fas fa-download"></i></span>
                    <span>Download File</span>
                `;
            }
            
            ProgressManager.update(100, 'Complete!');
            await new Promise(resolve => setTimeout(resolve, 500));
            
        } catch (error) {
            PreviewManager.showContent(`Error: ${error.message}`, exporter);
            NotificationManager.show(`Generation failed: ${error.message}`, 'danger');
            this.hasValidContent = false;
            this.downloadBtn.disabled = true;
        } finally {
            ProgressManager.hide();
        }
    }

    async downloadFile() {
        if (!this.hasValidContent) return;
        
        const path = this.pathInput.value.trim();
        const exporter = this.exporterSelect.value;
        
        try {
            // Show loading state
            this.downloadBtn.disabled = true;
            this.downloadBtn.className = 'button is-primary is-loading';
            
            ProgressManager.show('Preparing download...');
            const filename = await this.exporterService.downloadFile(path, exporter);
            
            // Success state
            this.downloadBtn.className = 'button is-success';
            this.downloadBtn.innerHTML = `
                <span class="icon"><i class="fas fa-check"></i></span>
                <span>Downloaded!</span>
            `;
            
            NotificationManager.show(`File "${filename}" downloaded successfully!`, 'success');
            
            // Reset button after 3 seconds
            setTimeout(() => {
                this.downloadBtn.disabled = false;
                this.downloadBtn.className = 'button is-primary';
                this.downloadBtn.innerHTML = `
                    <span class="icon"><i class="fas fa-download"></i></span>
                    <span>Download ${exporter.toUpperCase()} File</span>
                `;
            }, 3000);
            
        } catch (error) {
            NotificationManager.show(`Download failed: ${error.message}`, 'danger');
            this.downloadBtn.disabled = false;
            this.downloadBtn.className = 'button is-primary';
        } finally {
            ProgressManager.hide();
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const app = new VSSToolsApp();
    app.init();
});
