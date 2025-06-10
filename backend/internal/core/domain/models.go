package domain

import (
	"time"

	"github.com/google/uuid"
)

// Persona represents a saved AI configuration with a specific system prompt and parameters.
type Persona struct {
	ID           uuid.UUID `json:"id" db:"id"`
	Name         string    `json:"name" db:"name"`
	SystemPrompt string    `json:"system_prompt" db:"system_prompt"`
	MaxTokens    int       `json:"max_tokens" db:"max_tokens"`
	Temperature  float32   `json:"temperature" db:"temperature"`
	TopP         float32   `json:"top_p" db:"top_p"`
	CreatedAt    time.Time `json:"created_at" db:"created_at"`
	UpdatedAt    time.Time `json:"updated_at" db:"updated_at"`
}

// Conversation represents a single chat session.
type Conversation struct {
	ID        uuid.UUID `json:"id" db:"id"`
	Title     string    `json:"title" db:"title"`
	PersonaID uuid.UUID `json:"persona_id" db:"persona_id"`
	CreatedAt time.Time `json:"created_at" db:"created_at"`
	UpdatedAt time.Time `json:"updated_at" db:"updated_at"`
}

// Message represents a single message within a conversation.
type Message struct {
	ID             uuid.UUID `json:"id" db:"id"`
	ConversationID uuid.UUID `json:"conversation_id" db:"conversation_id"`
	Role           string    `json:"role" db:"role"` // e.g., "user", "assistant"
	Content        string    `json:"content" db:"content"`
	ModelUsed      string    `json:"model_used" db:"model_used"`
	CreatedAt      time.Time `json:"created_at" db:"created_at"`
}
