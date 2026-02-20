package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

func main() {
	log.Println("server start...")
	fs := http.FileServer(http.Dir("./static"))
	http.Handle("/", fs)
	http.HandleFunc("/upload", uploadFileHandler)
	if err := http.ListenAndServe(":3001", nil); err != nil {
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
