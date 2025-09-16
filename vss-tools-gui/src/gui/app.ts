import { PathInput } from './components/PathInput';
import { ExporterDropdown } from './components/ExporterDropdown';
import { FilePreview } from './components/FilePreview';
import { ExporterService } from './services/ExporterService';

export function initializeApp() {
    // Clear the body and add a title
    document.body.innerHTML = '<h1>VSS Tools GUI</h1>';
    
    const pathInput = new PathInput();
    const exporterDropdown = new ExporterDropdown();
    const filePreview = new FilePreview();
    const exporterService = new ExporterService();

    // Render components
    document.body.appendChild(pathInput.render());
    document.body.appendChild(exporterDropdown.render());
    document.body.appendChild(filePreview.render());

    // Function to update preview
    const updatePreview = async () => {
        const path = pathInput.getPath();
        const selectedExporter = exporterDropdown.getSelectedExporter();
        
        // Show loading message
        filePreview.updatePreview('Generating preview...');
        
        try {
            const content = await exporterService.generateFile(path, selectedExporter);
            filePreview.updatePreview(content);
        } catch (error) {
            filePreview.updatePreview(`Error: ${error instanceof Error ? error.message : String(error)}`);
        }
    };

    // Event listeners
    pathInput.onInputChange(updatePreview);
    exporterDropdown.onChange(updatePreview);
    
    // Initial preview
    updatePreview();
}