package postgres

import (
	"context"
	"fmt"
	"os"

	"github.com/devaldrete/kowai/internal/core/domain"
	"github.com/devaldrete/kowai/internal/core/ports"
	"github.com/google/uuid"
	"github.com/jackc/pgx/v5/pgxpool"
)

// PostgreSQLAdapter is the driven adapter for the database. It implements the DatabasePort
// interface and provides a concrete implementation for interacting with a PostgreSQL
// database using the pgx library. All methods for data persistence are defined here.
type PostgreSQLAdapter struct {
	pool *pgxpool.Pool
}

// NewPostgreSQLAdapter creates a new instance of the PostgreSQLAdapter.
// It initializes the database connection pool using the DATABASE_URL environment
// variable. It also pings the database to ensure a valid connection is established.
func NewPostgreSQLAdapter(ctx context.Context) (ports.DatabasePort, error) {
	connString := os.Getenv("DATABASE_URL")
	if connString == "" {
		fmt.Println("WARNING: DATABASE_URL environment variable not set. Using placeholder.")
		return &PostgreSQLAdapter{pool: nil}, nil
	}

	pool, err := pgxpool.New(ctx, connString)
	if err != nil {
		return nil, fmt.Errorf("unable to create connection pool: %w", err)
	}

	if err := pool.Ping(ctx); err != nil {
		pool.Close()
		return nil, fmt.Errorf("unable to ping database: %w", err)
	}

	return &PostgreSQLAdapter{pool: pool}, nil
}

// --- Persona Methods ---

// CreatePersona inserts a new persona record into the database.
func (a *PostgreSQLAdapter) CreatePersona(ctx context.Context, persona *domain.Persona) error {
	query := `
		INSERT INTO personas (id, name, system_prompt, max_tokens, temperature, top_p, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`
	_, err := a.pool.Exec(ctx, query,
		persona.ID,
		persona.Name,
		persona.SystemPrompt,
		persona.MaxTokens,
		persona.Temperature,
		persona.TopP,
		persona.CreatedAt,
		persona.UpdatedAt,
	)
	if err != nil {
		return fmt.Errorf("unable to create persona: %w", err)
	}
	return nil
}

// GetPersonaByID retrieves a single persona from the database by its UUID.
func (a *PostgreSQLAdapter) GetPersonaByID(ctx context.Context, id uuid.UUID) (*domain.Persona, error) {
	query := `
		SELECT id, name, system_prompt, max_tokens, temperature, top_p, created_at, updated_at
		FROM personas
		WHERE id = $1`
	var p domain.Persona
	err := a.pool.QueryRow(ctx, query, id).Scan(
		&p.ID,
		&p.Name,
		&p.SystemPrompt,
		&p.MaxTokens,
		&p.Temperature,
		&p.TopP,
		&p.CreatedAt,
		&p.UpdatedAt,
	)
	if err != nil {
		return nil, fmt.Errorf("unable to get persona by id: %w", err)
	}
	return &p, nil
}

// UpdatePersona updates an existing persona's details in the database.
func (a *PostgreSQLAdapter) UpdatePersona(ctx context.Context, persona *domain.Persona) error {
	query := `
		UPDATE personas
		SET name = $2, system_prompt = $3, max_tokens = $4, temperature = $5, top_p = $6, updated_at = $7
		WHERE id = $1`
	_, err := a.pool.Exec(ctx, query,
		persona.ID,
		persona.Name,
		persona.SystemPrompt,
		persona.MaxTokens,
		persona.Temperature,
		persona.TopP,
		persona.UpdatedAt,
	)
	if err != nil {
		return fmt.Errorf("unable to update persona: %w", err)
	}
	return nil
}

// DeletePersona removes a persona from the database by its UUID.
func (a *PostgreSQLAdapter) DeletePersona(ctx context.Context, id uuid.UUID) error {
	query := `DELETE FROM personas WHERE id = $1`
	_, err := a.pool.Exec(ctx, query, id)
	if err != nil {
		return fmt.Errorf("unable to delete persona: %w", err)
	}
	return nil
}

// ListPersonas retrieves all personas from the database, ordered by creation date.
func (a *PostgreSQLAdapter) ListPersonas(ctx context.Context) ([]*domain.Persona, error) {
	query := `
		SELECT id, name, system_prompt, max_tokens, temperature, top_p, created_at, updated_at
		FROM personas
		ORDER BY created_at DESC`
	rows, err := a.pool.Query(ctx, query)
	if err != nil {
		return nil, fmt.Errorf("unable to list personas: %w", err)
	}
	defer rows.Close()

	var personas []*domain.Persona
	for rows.Next() {
		var p domain.Persona
		if err := rows.Scan(
			&p.ID,
			&p.Name,
			&p.SystemPrompt,
			&p.MaxTokens,
			&p.Temperature,
			&p.TopP,
			&p.CreatedAt,
			&p.UpdatedAt,
		); err != nil {
			return nil, fmt.Errorf("unable to scan persona row: %w", err)
		}
		personas = append(personas, &p)
	}

	return personas, nil
}

// --- Conversation Methods ---

// CreateConversation inserts a new conversation record into the database.
func (a *PostgreSQLAdapter) CreateConversation(ctx context.Context, conversation *domain.Conversation) error {
	query := `
		INSERT INTO conversations (id, title, persona_id, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5)`
	_, err := a.pool.Exec(ctx, query,
		conversation.ID,
		conversation.Title,
		conversation.PersonaID,
		conversation.CreatedAt,
		conversation.UpdatedAt,
	)
	if err != nil {
		return fmt.Errorf("unable to create conversation: %w", err)
	}
	return nil
}

// GetConversationByID retrieves a single conversation from the database by its UUID.
func (a *PostgreSQLAdapter) GetConversationByID(ctx context.Context, id uuid.UUID) (*domain.Conversation, error) {
	query := `
		SELECT id, title, persona_id, created_at, updated_at
		FROM conversations
		WHERE id = $1`
	var c domain.Conversation
	err := a.pool.QueryRow(ctx, query, id).Scan(
		&c.ID,
		&c.Title,
		&c.PersonaID,
		&c.CreatedAt,
		&c.UpdatedAt,
	)
	if err != nil {
		return nil, fmt.Errorf("unable to get conversation by id: %w", err)
	}
	return &c, nil
}

// ListConversations retrieves all conversations from the database, ordered by last update.
func (a *PostgreSQLAdapter) ListConversations(ctx context.Context) ([]*domain.Conversation, error) {
	query := `
		SELECT id, title, persona_id, created_at, updated_at
		FROM conversations
		ORDER BY updated_at DESC`
	rows, err := a.pool.Query(ctx, query)
	if err != nil {
		return nil, fmt.Errorf("unable to list conversations: %w", err)
	}
	defer rows.Close()

	var conversations []*domain.Conversation
	for rows.Next() {
		var c domain.Conversation
		if err := rows.Scan(
			&c.ID,
			&c.Title,
			&c.PersonaID,
			&c.CreatedAt,
			&c.UpdatedAt,
		); err != nil {
			return nil, fmt.Errorf("unable to scan conversation row: %w", err)
		}
		conversations = append(conversations, &c)
	}

	return conversations, nil
}

// --- Message Methods ---

// CreateMessage inserts a new message record into the database.
func (a *PostgreSQLAdapter) CreateMessage(ctx context.Context, message *domain.Message) error {
	query := `
		INSERT INTO messages (id, conversation_id, role, content, model_used, created_at)
		VALUES ($1, $2, $3, $4, $5, $6)`
	_, err := a.pool.Exec(ctx, query,
		message.ID,
		message.ConversationID,
		message.Role,
		message.Content,
		message.ModelUsed,
		message.CreatedAt,
	)
	if err != nil {
		return fmt.Errorf("unable to create message: %w", err)
	}
	return nil
}

// GetMessagesByConversationID retrieves all messages for a specific conversation, ordered by creation date.
func (a *PostgreSQLAdapter) GetMessagesByConversationID(ctx context.Context, conversationID uuid.UUID) ([]*domain.Message, error) {
	query := `
		SELECT id, conversation_id, role, content, model_used, created_at
		FROM messages
		WHERE conversation_id = $1
		ORDER BY created_at ASC`
	rows, err := a.pool.Query(ctx, query, conversationID)
	if err != nil {
		return nil, fmt.Errorf("unable to get messages by conversation id: %w", err)
	}
	defer rows.Close()

	var messages []*domain.Message
	for rows.Next() {
		var m domain.Message
		if err := rows.Scan(
			&m.ID,
			&m.ConversationID,
			&m.Role,
			&m.Content,
			&m.ModelUsed,
			&m.CreatedAt,
		); err != nil {
			return nil, fmt.Errorf("unable to scan message row: %w", err)
		}
		messages = append(messages, &m)
	}

	return messages, nil
}
