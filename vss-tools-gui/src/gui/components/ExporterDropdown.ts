export class ExporterDropdown {
    private selectElement: HTMLSelectElement;
    private containerElement: HTMLDivElement;
    private exporters: string[] = [
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

    constructor() {
        this.containerElement = document.createElement('div');
        this.containerElement.className = 'exporter-dropdown-container';
        
        const label = document.createElement('label');
        label.textContent = 'Select Exporter:';
        label.htmlFor = 'exporter-select';
        
        this.selectElement = document.createElement('select');
        this.selectElement.id = 'exporter-select';
        
        // Add options
        this.exporters.forEach(exporter => {
            const option = document.createElement('option');
            option.value = exporter;
            option.textContent = exporter;
            this.selectElement.appendChild(option);
        });
        
        this.containerElement.appendChild(label);
        this.containerElement.appendChild(this.selectElement);
    }

    public render(): HTMLDivElement {
        return this.containerElement;
    }

    public getSelectedExporter(): string {
        return this.selectElement.value;
    }

    public onChange(callback: () => void): void {
        this.selectElement.addEventListener('change', callback);
    }
}