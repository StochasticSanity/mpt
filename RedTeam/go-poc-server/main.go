package main

import (
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"

	"github.com/gorilla/mux"
)

func main() {
	// Create a new router
	router := mux.NewRouter()

	// Handle the root route
	router.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// Parse the query parameters
		query := r.URL.Query()
		hostname := query.Get("hostname")
		username := query.Get("username")

		// Print the received request with colors
		fmt.Printf("\033[32mReceived request:\033[0m \033[33m%s %s\033[0m\n", r.Method, r.URL.String())
		fmt.Printf("  \033[35mhostname:\033[0m %s\n", hostname)
		fmt.Printf("  \033[35musername:\033[0m %s\n", username)
	})

	// Create a new server
	server := &http.Server{
		Addr:    ":8080",
		Handler: router,
	}

	// Start the server in a separate goroutine
	go func() {
		fmt.Println("Server listening on port 8080")
		if err := server.ListenAndServe(); err != nil {
			if err == http.ErrServerClosed {
				fmt.Println("Server stopped")
			} else {
				panic(err)
			}
		}
	}()

	// Wait for a SIGINT or SIGTERM signal to stop the server
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGINT, syscall.SIGTERM)
	<-stop

	// Stop the server gracefully
	fmt.Println("Stopping server...")
	if err := server.Shutdown(nil); err != nil {
		panic(err)
	}
}
