# This is going to be a very big file, but it will be divided into other files, but for
# now, for the sake of simplicity, let's build it like this!

import datetime
import enum
from uuid import uuid4
from sqlalchemy import (
    DECIMAL,
    TIMESTAMP,
    VARCHAR,
    Column,
    DateTime,
    Table,
    Text,
    ForeignKey,
    Boolean,
    UUID,
    Enum as SQLAEnum,
    Integer,
    Index,
)
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.functions import now
from typing import Optional


class Base(DeclarativeBase):
    pass


# Enums
class ProviderType(enum.Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    VERTEX = "vertex"
    GEMINI = "gemini"
    OPENROUTER = "openrouter"
    AZURE = "azure"
    GROQ = "groq"
    GROK = "grok"
    OLLAMA = "ollama"


class MessageRole(enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class SubscriptionStatus(enum.Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    EXPIRED = "expired"
    TRIAL = "trial"
    PAST_DUE = "past_due"
    UNPAID = "unpaid"
    INCOMPLETE = "incomplete"
    INCOMPLETE_EXPIRED = "incomplete_expired"
    PAUSED = "paused"


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"
    REFUNDED = "refunded"


# Association Tables
role_user = Table(
    "role_user",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)

agent_prompt = Table(
    "agent_prompt",
    Base.metadata,
    Column("agent_id", ForeignKey("agents.id"), primary_key=True),
    Column("prompt_id", ForeignKey("prompts.id"), primary_key=True),
    Column("created_at", TIMESTAMP(timezone=True), default=now()),
    Column("updated_at", TIMESTAMP(timezone=True), default=now(), onupdate=now()),
)


# RBAC System
class Role(Base):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    name: Mapped[str] = mapped_column(VARCHAR(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(VARCHAR(200))
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=now()
    )

    users: Mapped[list["User"]] = relationship(
        secondary=role_user,
        back_populates="roles",
    )


# AI Agents Logic
class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(VARCHAR(500))
    provider: Mapped[ProviderType] = mapped_column(
        SQLAEnum(ProviderType),
        default=ProviderType.OPENAI,
    )
    model_name: Mapped[Optional[str]] = mapped_column(VARCHAR(100))
    temperature: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 2), default=0.7)
    max_tokens: Mapped[Optional[int]] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=now(), onupdate=now()
    )

    prompts: Mapped[list["Prompt"]] = relationship(
        secondary=agent_prompt,
        back_populates="agents",
    )
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="agent")
    creator: Mapped["User"] = relationship(back_populates="created_agents")


class Prompt(Base):
    __tablename__ = "prompts"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    created_by: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=now(), onupdate=now()
    )

    agents: Mapped[list["Agent"]] = relationship(
        secondary=agent_prompt,
        back_populates="prompts",
    )
    creator: Mapped["User"] = relationship(back_populates="created_prompts")


# Improved Chat Logic
class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    title: Mapped[Optional[str]] = mapped_column(VARCHAR(200))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    agent_id: Mapped[UUID] = mapped_column(ForeignKey("agents.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=now(), onupdate=now()
    )

    user: Mapped["User"] = relationship(back_populates="conversations")
    agent: Mapped["Agent"] = relationship(back_populates="conversations")
    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("idx_conversation_user_created", "user_id", "created_at"),)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    conversation_id: Mapped[UUID] = mapped_column(
        ForeignKey("conversations.id"), nullable=False
    )
    role: Mapped[MessageRole] = mapped_column(SQLAEnum(MessageRole), nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    token_count: Mapped[Optional[int]] = mapped_column(Integer)
    is_deleted: Mapped[bool] = mapped_column(Boolean(), default=False)
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=now(), onupdate=now()
    )
    deleted_at: Mapped[Optional[DateTime]] = mapped_column(TIMESTAMP(timezone=True))

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")

    __table_args__ = (
        Index("idx_message_conversation_created", "conversation_id", "created_at"),
    )


# Enhanced User Management
class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    appwrite_user_id: Mapped[str] = mapped_column(
        VARCHAR(255), unique=True, nullable=False
    )  # Link to Appwrite
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(VARCHAR(255), unique=True)
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(VARCHAR(500))
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    trial_ends_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        TIMESTAMP(timezone=True)
    )
    subscription_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("subscriptions.id")
    )
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=now(), onupdate=now()
    )
    last_login: Mapped[Optional[DateTime]] = mapped_column(TIMESTAMP(timezone=True))

    subscription: Mapped[Optional["SubscriptionPlan"]] = relationship(
        back_populates="users"
    )
    roles: Mapped[list["Role"]] = relationship(
        secondary=role_user,
        back_populates="users",
    )
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="user")
    created_agents: Mapped[list["Agent"]] = relationship(back_populates="creator")
    created_prompts: Mapped[list["Prompt"]] = relationship(back_populates="creator")
    usage_logs: Mapped[list["UsageLog"]] = relationship(back_populates="user")

    __table_args__ = (
        Index("idx_user_appwrite_id", "appwrite_user_id"),
        Index("idx_user_email", "email"),
    )


class SubscriptionPlan(Base):
    __tablename__ = "subscriptions"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    stripe_price_id: Mapped[str] = mapped_column(
        VARCHAR(255), unique=True, nullable=True
    )
    stripe_product_id: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    name: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(VARCHAR(300))
    price: Mapped[DECIMAL] = mapped_column(DECIMAL(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(VARCHAR(3), default="USD")
    billing_interval: Mapped[str] = mapped_column(
        VARCHAR(20), default="monthly"
    )  # monthly, yearly
    max_conversations: Mapped[Optional[int]] = mapped_column(Integer)
    max_messages_per_month: Mapped[Optional[int]] = mapped_column(Integer)
    max_tokens_per_month: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[SubscriptionStatus] = mapped_column(
        SQLAEnum(SubscriptionStatus), default=SubscriptionStatus.TRIAL
    )
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=now(), onupdate=now()
    )

    users: Mapped[list["User"]] = relationship(back_populates="subscription")


# Usage tracking for billing/analytics
class UsageLog(Base):
    __tablename__ = "usage_logs"

    id: Mapped[UUID] = mapped_column(primary_key=True, default_factory=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    conversation_id: Mapped[UUID] = mapped_column(
        ForeignKey("conversations.id"), nullable=False
    )
    tokens_used: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[Optional[DECIMAL]] = mapped_column(DECIMAL(10, 6))  # Cost in cents
    provider: Mapped[ProviderType] = mapped_column(
        SQLAEnum(ProviderType), nullable=False
    )
    model_name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), default=now()
    )

    user: Mapped["User"] = relationship(back_populates="usage_logs")

    __table_args__ = (Index("idx_usage_user_date", "user_id", "created_at"),)
