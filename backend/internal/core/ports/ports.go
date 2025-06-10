package ports

import (
	"context"

	"github.com/google/uuid"

	"github.com/devaldrete/kowai/internal/core/domain"
)

// ConversationManager defines the port for managing conversations.
// This interface will be implemented by a service in the core.
type ConversationManager interface {
	// Add methods here later, e.g., StartConversation, PostMessage, etc.
}

// PersonaManager defines the port for managing AI personas.
type PersonaManager interface {
	// Add methods here later, e.g., CreatePersona, GetPersona, etc.
}

// LLMProvider defines the port for interacting with an external LLM.
type LLMProvider interface {
	GenerateStream(ctx context.Context, messages []domain.Message) (<-chan string, error)
}

// ConversationRepository defines the port for conversation persistence.
type ConversationRepository interface {
	// Add methods for DB interaction, e.g., SaveMessage, GetHistory, etc.
}

// DatabasePort defines the contract for database operations.
// This will be implemented by a driven adapter (e.g., PostgreSQL).
type DatabasePort interface {
	// Persona Methods
	CreatePersona(ctx context.Context, persona *domain.Persona) error
	GetPersonaByID(ctx context.Context, id uuid.UUID) (*domain.Persona, error)
	UpdatePersona(ctx context.Context, persona *domain.Persona) error
	DeletePersona(ctx context.Context, id uuid.UUID) error
	ListPersonas(ctx context.Context) ([]*domain.Persona, error)

	// Conversation Methods
	CreateConversation(ctx context.Context, conversation *domain.Conversation) error
	GetConversationByID(ctx context.Context, id uuid.UUID) (*domain.Conversation, error)
	ListConversations(ctx context.Context) ([]*domain.Conversation, error)

	// Message Methods
	CreateMessage(ctx context.Context, message *domain.Message) error
	GetMessagesByConversationID(ctx context.Context, conversationID uuid.UUID) ([]*domain.Message, error)
}
