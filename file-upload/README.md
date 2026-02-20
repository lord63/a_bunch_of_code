# File Upload Service

A simple file upload service built with Go and [FilePond](https://pqina.nl/filepond/).

## Features

- **Backend**: Go `net/http` providing a static file server and an upload endpoint.
- **Frontend**: A minimal HTML page using the FilePond library to handle drag-and-drop file uploads.
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
2. Start the Go server:
   ```bash
   go run main.go
   ```
3. Open your browser and navigate to [http://localhost:3001](http://localhost:3001).
4. Drag and drop files into the FilePond interface to upload them.

## API Endpoints

### `POST /upload`
- Accepts `multipart/form-data`.
- Expects the file input to be named `filepond`.
- Saves the received file directly to the `./uploads/` directory using its original filename.
