# File Upload Service

A simple file upload service built with Go and [FilePond](https://pqina.nl/filepond/).

## Features

- **Backend**: Go `net/http` providing an upload endpoint and serving static files using `go:embed`.
- **Frontend**: A minimal HTML page using the FilePond library, which is embedded into the Go binary for single-executable deployment.
- **Storage**: Uploaded files are saved locally in the `uploads/` directory.

## Project Structure

```text
file-upload/
├── main.go          # Go backend server
├── static/          # Frontend static files
│   └── index.html   # FilePond interface
└── uploads/         # Directory for uploaded files
```

## Getting Started

### Prerequisites

- Go installed on your machine.

### Running the Server

1. Make sure you are in the `file-upload` directory.
2. Run the server (or build the binary with `go build` for a single-file deployment):
   ```bash
   go run main.go
   ```
3. Open your browser and navigate to [http://localhost:3001](http://localhost:3001).
4. Drag and drop files into the FilePond interface to upload them.

