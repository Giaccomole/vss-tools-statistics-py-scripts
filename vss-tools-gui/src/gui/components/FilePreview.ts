export class FilePreview {
    private previewElement: HTMLDivElement;

    constructor() {
        this.previewElement = document.createElement('div');
        this.previewElement.className = 'file-preview';
    }

    public render(): HTMLDivElement {
        return this.previewElement;
    }

    public updatePreview(content: string): void {
        this.previewElement.textContent = content;
    }
}