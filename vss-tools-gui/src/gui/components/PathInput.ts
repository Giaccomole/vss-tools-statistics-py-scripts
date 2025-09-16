export class PathInput {
    private inputElement: HTMLInputElement;
    private containerElement: HTMLDivElement;

    constructor() {
        this.containerElement = document.createElement('div');
        this.containerElement.className = 'path-input-container';
        
        const label = document.createElement('label');
        label.textContent = 'VSS File Path:';
        label.htmlFor = 'path-input';
        
        this.inputElement = document.createElement('input');
        this.inputElement.type = 'text';
        this.inputElement.id = 'path-input';
        this.inputElement.placeholder = 'Enter path to vspec file...';
        
        this.containerElement.appendChild(label);
        this.containerElement.appendChild(this.inputElement);
    }

    public render(): HTMLDivElement {
        return this.containerElement;
    }

    public getPath(): string {
        return this.inputElement.value;
    }

    public onInputChange(callback: () => void): void {
        this.inputElement.addEventListener('input', callback);
    }
}