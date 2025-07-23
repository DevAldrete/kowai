from enum import Enum

import dspy
from pydantic import BaseModel


class ProviderType(Enum):
    """Enum for AI providers"""

    OPENAI = "openai"
    AZURE = "azure"
    AWS = "aws"
    HUGGINGFACE = "huggingface"
    COHERE = "cohere"
    ANTHROPIC = "anthropic"
    MISTRAL = "mistral"
    GROQ = "groq"
    GROK = "grok"
    GOOGLE = "google"
    LOCAL = "local"
    OPENROUTER = "openrouter"


class Metadata(BaseModel):
    """Metadata for AI agent management"""

    model: str
    tokens: int
    temperature: float
    max_tokens: int
    model: str
    provider: ProviderType
    api_key: str | None = None
    base_url: str | None = None


class Management:
    """Management class for AI agents"""

    def __init__(self, metadata: Metadata):
        self.metadata = metadata

    def get_metadata(self) -> Metadata:
        """Get metadata of the AI agent"""
        return self.metadata

    def set_metadata(self, metadata: Metadata):
        """Set metadata for the AI agent"""
        self.metadata = metadata

    def update_metadata(self, **kwargs):
        """Update metadata with provided keyword arguments"""
        for key, value in kwargs.items():
            if hasattr(self.metadata, key):
                setattr(self.metadata, key, value)
            else:
                err = f"Invalid metadata field: {key}"
                raise ValueError(err)

    def get_lm(self):
        """Get the language model instance"""
        return dspy.LM(
            self.metadata.model,
            max_tokens=self.metadata.max_tokens,
            temperature=self.metadata.temperature,
            provider=self.metadata.provider.value,
            api_key=self.metadata.api_key,
            base_url=self.metadata.base_url,
        )
