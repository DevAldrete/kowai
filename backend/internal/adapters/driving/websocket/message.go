package websocket

type IncomingMessage struct {
	Type           string      `json:"type"`
	Payload        interface{} `json:"payload"`
	ConversationID string      `json:"conversationId"`
}

type OutgoingMessage struct {
	Type    string      `json:"type"`
	Payload interface{} `json:"payload"`
}
