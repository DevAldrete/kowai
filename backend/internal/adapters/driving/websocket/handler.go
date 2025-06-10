package websocket

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
	"time"

	"github.com/devaldrete/kowai/internal/core/domain"
	"github.com/devaldrete/kowai/internal/core/ports"
	"github.com/google/uuid"
	"github.com/gorilla/websocket"
)

const (
	writeWait      = 10 * time.Second
	pongWait       = 60 * time.Second
	pingPeriod     = (pongWait * 9) / 10
	maxMessageSize = 512
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		// Allow all connections for now
		return true
	},
}

// Client represents a single WebSocket connection.
type Client struct {
	hub  *Hub
	ID   string
	Conn *websocket.Conn
	Send chan []byte
}

// Hub maintains the set of active clients and broadcasts messages.
type Hub struct {
	Clients    map[string]*Client
	Register   chan *Client
	Unregister chan *Client
	Broadcast  chan []byte
	mu         sync.Mutex
}

func NewHub() *Hub {
	return &Hub{
		Clients:    make(map[string]*Client),
		Register:   make(chan *Client),
		Unregister: make(chan *Client),
		Broadcast:  make(chan []byte),
	}
}

func (h *Hub) Run() {
	for {
		select {
		case client := <-h.Register:
			h.mu.Lock()
			h.Clients[client.ID] = client
			h.mu.Unlock()
		case client := <-h.Unregister:
			h.mu.Lock()
			if _, ok := h.Clients[client.ID]; ok {
				delete(h.Clients, client.ID)
				close(client.Send)
			}
			h.mu.Unlock()
		case message := <-h.Broadcast:
			h.mu.Lock()
			for _, client := range h.Clients {
				select {
				case client.Send <- message:
				default:
					close(client.Send)
					delete(h.Clients, client.ID)
				}
			}
			h.mu.Unlock()
		}
	}
}

type WebSocketHandler struct {
	hub         *Hub
	llmProvider ports.LLMProvider
}

func NewWebSocketHandler(hub *Hub, llmProvider ports.LLMProvider) *WebSocketHandler {
	return &WebSocketHandler{
		hub:         hub,
		llmProvider: llmProvider,
	}
}

func (h *WebSocketHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		fmt.Printf("Failed to upgrade connection: %v\n", err)
		http.Error(w, "Could not open websocket connection", http.StatusBadRequest)
		return
	}

	client := &Client{
		hub:  h.hub,
		ID:   uuid.New().String(),
		Conn: conn,
		Send: make(chan []byte, 256),
	}
	h.hub.Register <- client

	go client.writePump()
	go client.readPump(h)

	// We will add read/write pump logic in a later step
	// For now, this sets up the connection management.
	fmt.Printf("Client connected: %s\n", client.ID)
}

func (c *Client) readPump(h *WebSocketHandler) {
	defer func() {
		c.hub.Unregister <- c
		c.Conn.Close()
	}()
	c.Conn.SetReadLimit(maxMessageSize)
	c.Conn.SetReadDeadline(time.Now().Add(pongWait))
	c.Conn.SetPongHandler(func(string) error { c.Conn.SetReadDeadline(time.Now().Add(pongWait)); return nil })
	for {
		_, message, err := c.Conn.ReadMessage()
		if err != nil {
			if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
				fmt.Printf("error: %v\n", err)
			}
			break
		}
		var incomingMessage IncomingMessage
		if err := json.Unmarshal(message, &incomingMessage); err != nil {
			fmt.Printf("error unmarshalling message: %v\n", err)
			c.sendErrorMessage("Invalid message format")
			continue
		}
		h.handleMessage(c, incomingMessage)
	}
}

func (c *Client) writePump() {
	ticker := time.NewTicker(pingPeriod)
	defer func() {
		ticker.Stop()
		c.Conn.Close()
	}()
	for {
		select {
		case message, ok := <-c.Send:
			c.Conn.SetWriteDeadline(time.Now().Add(writeWait))
			if !ok {
				c.Conn.WriteMessage(websocket.CloseMessage, []byte{})
				return
			}
			w, err := c.Conn.NextWriter(websocket.TextMessage)
			if err != nil {
				fmt.Printf("error getting next writer: %v\n", err)
				return
			}
			w.Write(message)
			if err := w.Close(); err != nil {
				fmt.Printf("error closing writer: %v\n", err)
				return
			}
		case <-ticker.C:
			c.Conn.SetWriteDeadline(time.Now().Add(writeWait))
			if err := c.Conn.WriteMessage(websocket.PingMessage, nil); err != nil {
				return
			}
		}
	}
}

func (h *WebSocketHandler) handleMessage(client *Client, message IncomingMessage) {
	switch message.Type {
	case "chat":
		if text, ok := message.Payload.(string); ok {
			messages := []domain.Message{{Role: "user", Content: text}}
			stream, err := h.llmProvider.GenerateStream(context.Background(), messages)
			if err != nil {
				fmt.Printf("error generating stream: %v\n", err)
				client.sendErrorMessage("Failed to generate response from LLM")
				return
			}

			for content := range stream {
				outgoingMessage := OutgoingMessage{Type: "stream", Payload: content}
				jsonMessage, _ := json.Marshal(outgoingMessage)
				client.Send <- jsonMessage
			}
		} else {
			client.sendErrorMessage("Invalid payload for chat message")
		}
	default:
		client.sendErrorMessage("Unknown message type")
	}
}

func (c *Client) sendErrorMessage(message string) {
	msg := OutgoingMessage{
		Type:    "error",
		Payload: message,
	}
	jsonMsg, _ := json.Marshal(msg)
	c.Send <- jsonMsg
}
