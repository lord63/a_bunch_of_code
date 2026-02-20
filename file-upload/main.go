package main

import (
	"embed"
	"flag"
	"fmt"
	"io"
	"io/fs"
	"log"
	"net/http"
	"os"
)

//go:embed static/*
var staticFiles embed.FS

var version = "0.2.0"

func main() {
	port := flag.String("port", "3001", "port to run the server on")
	v := flag.Bool("version", false, "display version and exit")
	flag.Parse()

	if *v {
		fmt.Printf("file-upload v%s\n", version)
		os.Exit(0)
	}

	log.Printf("server start on port %s...\n", *port)

	staticFS, err := fs.Sub(staticFiles, "static")
	if err != nil {
		log.Fatal(err)
	}

	fs := http.FileServer(http.FS(staticFS))
	http.Handle("/", fs)
	http.HandleFunc("/upload", uploadFileHandler)
	if err := http.ListenAndServe(":"+*port, nil); err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}

func uploadFileHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("receive req")
	// Get file from upload input
	file, header, err := r.FormFile("filepond")
	if err != nil {
		http.Error(w, "Bad request", http.StatusBadRequest)
		return
	}
	defer file.Close()

	// Save file to server
	if err := os.MkdirAll("./uploads", 0755); err != nil {
		http.Error(w, fmt.Sprintf("Unable to create uploads directory, err:%s", err), http.StatusInternalServerError)
		return
	}
	filename := header.Filename
	out, err := os.Create("./uploads/" + filename)
	if err != nil {
		http.Error(w, fmt.Sprintf("Unable to create file, err:%s", err), http.StatusInternalServerError)
		return
	}
	defer out.Close()
	_, err = io.Copy(out, file)
	if err != nil {
		http.Error(w, fmt.Sprintf("Unable to save file, err:%s", err), http.StatusInternalServerError)
		return
	}

	w.Write([]byte("File uploaded successfully"))
}
