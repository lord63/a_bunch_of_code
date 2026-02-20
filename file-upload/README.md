# File Upload Service

A simple file upload service built with Go and [FilePond](https://pqina.nl/filepond/). A common use case is uplaod files to your server.

![img](https://github.com/user-attachments/assets/f094eae9-e05d-40a7-b41a-33f70895d724)

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

You can download the compiled tarball directly, extract it, and run the binary. The download package contains the `file-upload` binary.

### Installation

1. Go to the [Releases](https://github.com/lord63/a_bunch_of_code/releases) page and download the `.tar.gz` for your platform (e.g., `file-upload-linux-amd64.tar.gz`).
2. Extract the archive:
   ```bash
   tar -xzf file-upload-linux-amd64.tar.gz
   ```
3. Run the extracted binary:
   ```bash
   ./file-upload
   ```

### Usage

The binary accepts the following flags:

- `-port`: The port to run the server on (default `"3001"`).
- `-version`: Display version information and exit.

**Example**:
```bash
./file-upload -port 8080
```

Once running, navigate to `http://localhost:<port>` in your browser and drag/drop files to upload. Uploaded files will be automatically placed in an `uploads/` directory inside your current working directory.
