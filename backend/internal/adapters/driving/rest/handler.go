package http

import (
	"encoding/json"
	"net/http"
)

type HTTPHandler struct {
	// Add dependencies here later, e.g., ConfigProvider
}

func NewHTTPHandler() *HTTPHandler {
	return &HTTPHandler{}
}

func (h *HTTPHandler) RegisterRoutes(mux *http.ServeMux) {
	mux.HandleFunc("/api/config", h.GetConfig)
}

func (h *HTTPHandler) GetConfig(w http.ResponseWriter, r *http.Request) {
	config := struct {
		Model   string `json:"model"`
		Version string `json:"version"`
	}{
		Model:   "gpt-4o",
		Version: "1.0.0",
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(config)
}
