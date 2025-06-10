package openai

import (
	"context"
	"errors"
	"fmt"
	"io"

	"github.com/devaldrete/kowai/internal/core/domain"
	"github.com/sashabaranov/go-openai"
)

// OpenAIAdapter is the adapter for the OpenAI API.
type OpenAIAdapter struct {
	client *openai.Client
}

// NewOpenAIAdapter creates a new OpenAIAdapter.
func NewOpenAIAdapter(apiKey string) *OpenAIAdapter {
	return &OpenAIAdapter{
		client: openai.NewClient(apiKey),
	}
}

// GenerateStream handles the streaming logic with the OpenAI Go SDK.
func (a *OpenAIAdapter) GenerateStream(ctx context.Context, messages []domain.Message) (<-chan string, error) {
	out := make(chan string)

	// Map domain messages to OpenAI messages
	var openaiMessages []openai.ChatCompletionMessage
	for _, msg := range messages {
		openaiMessages = append(openaiMessages, openai.ChatCompletionMessage{
			Role:    msg.Role,
			Content: msg.Content,
		})
	}

	req := openai.ChatCompletionRequest{
		Model:    openai.GPT4o,
		Messages: openaiMessages,
		Stream:   true,
	}

	stream, err := a.client.CreateChatCompletionStream(ctx, req)
	if err != nil {
		return nil, fmt.Errorf("failed to create chat completion stream: %w", err)
	}

	go func() {
		defer stream.Close()
		defer close(out)

		for {
			response, err := stream.Recv()
			if errors.Is(err, io.EOF) {
				// Stream finished successfully
				return
			}
			if err != nil {
				// An error occurred during streaming.
				// It's important to handle this, perhaps by sending an error message
				// on a separate channel or logging it. For now, we'll just log and exit.
				// In a real application, you might want more sophisticated error handling.
				fmt.Printf("Error receiving stream response: %v\n", err)
				return
			}

			if len(response.Choices) > 0 {
				content := response.Choices[0].Delta.Content
				if content != "" {
					out <- content
				}
			}
		}
	}()

	return out, nil
}
