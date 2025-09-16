# vss-tools-gui

This project is a graphical user interface (GUI) for the VSS tools, designed to facilitate the export of vspec files into various formats. The application allows users to input a file path, select an exporter from a dropdown menu, and preview the generated file content.

## Project Structure

```
vss-tools-gui
├── src
│   ├── main.ts               # Entry point of the application
│   ├── gui
│   │   ├── components
│   │   │   ├── PathInput.ts  # Component for path input
│   │   │   ├── ExporterDropdown.ts # Component for selecting exporters
│   │   │   └── FilePreview.ts # Component for previewing generated file
│   │   ├── services
│   │   │   └── ExporterService.ts # Service for handling export logic
│   │   └── app.ts            # Initializes the main application
│   └── types
│       └── index.ts          # Type definitions for the project
├── package.json               # npm configuration file
├── tsconfig.json              # TypeScript configuration file
└── README.md                  # Project documentation
```

## Features

- **Path Input**: Users can enter the path of the vspec file they wish to export.
- **Exporter Selection**: A dropdown menu allows users to select from various available exporters.
- **File Preview**: Users can preview the content of the generated file in text format before exporting.

## Getting Started

1. Clone the repository:
   ```
   git clone <repository-url>
   cd vss-tools-gui
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the application:
   ```
   npm start
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the Mozilla Public License 2.0. See the LICENSE file for details.