package main

import (
	"fmt"
	"net/http"

	"github.com/devaldrete/kowai/internal/adapters/driven/openai"
	restHandler "github.com/devaldrete/kowai/internal/adapters/driving/rest"
	"github.com/devaldrete/kowai/internal/adapters/driving/websocket"
)

func main() {
	fmt.Println("KowAI Backend Starting...")

	// Create a new ServeMux
	mux := http.NewServeMux()

	// Initialize the driven adapters
	openaiAdapter := openai.NewOpenAIAdapter("YOUR_OPENAI_API_KEY")

	// Initialize the driving adapters
	hub := websocket.NewHub()
	go hub.Run()

	httpHandler := restHandler.NewHTTPHandler()
	httpHandler.RegisterRoutes(mux)

	websocketHandler := websocket.NewWebSocketHandler(hub, openaiAdapter)
	mux.Handle("/ws", websocketHandler)

	// Start the server
	fmt.Println("Server is running on port 8080")
	if err := http.ListenAndServe(":8080", mux); err != nil {
		fmt.Printf("could not start server: %v\n", err)
	}
}
