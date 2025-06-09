# KowAI 👻

<div align="center">
  <!-- Suggestion: Create a simple, friendly ghost logo or a stylized "K" -->
  <img src="[YOUR_LOGO_URL_HERE]" alt="KowAI Logo" width="150"/>
  <h1>KowAI</h1>
  <p>
    <strong>The scary-good, self-hostable AI chat platform for power-users.</strong>
  </p>
  <p>
    Take back control of your AI interactions. Host your own secure, high-performance chat interface, connect to any LLM with your own keys, and forge personalized AI agents for any task imaginable.
  </p>
  <p>
    <!-- Replace with your actual repo and server details -->
    <a href="https://github.com/your-username/kowai/actions/workflows/ci.yml"><img src="https://github.com/your-username/kowai/actions/workflows/ci.yml/badge.svg" alt="Build Status"></a>
    <a href="https://github.com/your-username/kowai/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
    <a href="https://github.com/your-username/kowai/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
    <a href="https://discord.gg/[YOUR_DISCORD_INVITE]"><img src="https://img.shields.io/discord/[YOUR_DISCORD_SERVER_ID]?color=7289DA&label=Join%20Our%20Community&logo=discord&logoColor=white" alt="Join our Discord"></a>
  </p>
</div>

## ✨ Key Features

- 🔐 **Truly Self-Hosted & Private**: Run KowAI on your own infrastructure with Docker. Your conversations and API keys are yours alone. No tracking, no third-party data access.
- 🤖 **Multi-Model & Provider-Agnostic**: Connect to a wide range of LLM providers (OpenAI, Anthropic, Google, Groq) or even local models through services like Ollama. Switch between models on the fly.
- 🛠️ **Deep AI Personalization**: Go beyond basic prompts. Control core model parameters like `temperature`, `top_p`, and `max_tokens`. Craft unique AI "Personas" with custom system instructions and save them for later use.
- ⚡ **Blazing Fast & Responsive**: Built with a high-performance Go backend and a modern Angular frontend, KowAI is designed for speed. Responses are streamed in real-time for a seamless chat experience.
- 📖 **Markdown & Code Rendering**: Beautifully formatted responses with syntax highlighting for code blocks, making it a perfect tool for developers.
- 🏛️ **Built on Clean Architecture**: The Hexagonal (Ports & Adapters) architecture makes the codebase clean, testable, and easy to extend with new features or AI providers.

## 🏛️ Tech Stack & Architecture

KowAI is built on a robust, modern, and scalable technology stack, with a strong emphasis on separation of concerns.

| Component      | Technology                             | Rationale                                                                                     |
| -------------- | -------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Backend**    | **Go (Golang)**                        | Extreme performance, excellent concurrency for WebSockets, and single-binary deployments.     |
| **Frontend**   | **Angular** with **Analog.js**         | A structured, powerful framework with SSR capabilities for a fast and modern user experience. |
| **Database**   | **Neon** (Serverless PostgreSQL)       | Highly scalable, developer-friendly PostgreSQL that scales to zero. Perfect for self-hosting. |
| **Real-time**  | **WebSockets**                         | Low-latency, bidirectional communication for a fluid, real-time chat experience.              |
| **Deployment** | **Docker** & **Nginx** (Reverse Proxy) | Easy, reproducible deployments for any environment and efficient handling of web traffic.     |

### Hexagonal Architecture (Ports & Adapters)

The backend is designed using the Hexagonal Architecture to keep the core application logic decoupled from external technologies. This makes the system highly maintainable and extensible.

- **The Core (Hexagon)**: Contains the pure business logic of the application (e.g., managing conversations, creating personas). It has no knowledge of databases or external APIs.
- **Ports**: Simple interfaces defined by the Core that dictate how it interacts with the outside world (e.g., `ConversationRepositoryPort`, `LLMProviderPort`).
- **Adapters**: The concrete implementations of the Ports.
  - **Driving Adapters**: Trigger actions in the Core (e.g., REST API handlers, WebSocket controllers).
  - **Driven Adapters**: Are called by the Core to interact with external tools (e.g., a PostgreSQL adapter, an OpenAI API client adapter).

```plaintext
      +--------------------------------------------------+
      |                 Driving Adapters                 |
      |  (REST API, WebSocket Controller, CLI)           |
      +----------------------+---------------------------+
                             | (invokes)
                             v
+----------------------------------------------------------+
|   Ports (Interfaces defined by the Core Application)     |
|----------------------------------------------------------|
|                                                          |
|                  CORE APPLICATION LOGIC                  |
|                  (The Business Rules)                    |
|                                                          |
|----------------------------------------------------------|
|   Ports (Interfaces defined by the Core Application)     |
+----------------------------------------------------------+
                             | (invokes)
                             v
      +----------------------+---------------------------+
      |                  Driven Adapters                 |
      |  (PostgreSQL DB, OpenAI API, Anthropic API)      |
      +--------------------------------------------------+
```

## 🚀 Getting Started

You can get a local instance of KowAI running in minutes using Docker.

### Prerequisites

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/kowai.git
    cd kowai
    ```

2.  **Configure your environment:**
    Copy the example environment file. This is where you'll put your secret keys.

    ```sh
    cp .env.example .env
    ```

    Now, open the `.env` file with a text editor and add your database connection string and the API keys for the AI models you want to use.

3.  **Launch the application:**
    Use Docker Compose to build and run the entire stack (Go backend, Angular frontend, and Nginx).

    ```sh
    docker-compose up -d
    ```

    The `-d` flag runs the containers in detached mode.

4.  **You're live!**
    Open your browser and navigate to `http://localhost:8080` to start using your private KowAI instance.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. We welcome any and all contributions!

Please read our `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
