# KowAI Frontend Documentation

<div align="center">

![KowAI Frontend](https://img.shields.io/badge/KowAI-Frontend_Documentation-FF3E00?style=for-the-badge&logo=svelte&logoColor=white)

_Your guide to understanding, developing, and contributing to the KowAI frontend._

</div>

## 1. Project Overview

This document provides a comprehensive overview of the KowAI frontend, built with React, TailwindCSS, and other modern technologies. It serves as a guide for developers to understand the project structure, development workflow, and best practices.

### 1.1. Technology Stack

- Vite + React 19: A modern combination for building efficient and excellent pages!
- **[TailwindCSS 4](https://tailwindcss.com/)**: A utility-first CSS framework for rapid UI development.
- Aceternity UI: A modern library of pre-built components built with TailwindCSS.
- **[TanStack Query](https://tanstack.com/query)**: A powerful data fetching and caching library.
- **[TypeScript](https://www.typescriptlang.org/)**: A statically typed superset of JavaScript that enhances code quality and maintainability.
- TanStack Router: For a better routes management.

## 2. Project Structure

The project follows a standard React application structure, with some additional conventions for organizing components, stores, and utilities.

```
src/
├── routes/                     # Page routes and layouts
├── lib/
│   ├── components/             # Reusable Svelte components
│   │   ├── ui/                 # Base UI components (Button, Card, etc.)
│   │   ├── chat/               # Chat-specific components
│   │   ├── auth/               # Authentication components
│   │   └── layout/             # Layout components (Header, Footer, etc.)
│   ├── stores/                 # Svelte stores for state management
│   ├── utils/                  # Utility functions
│   ├── types/                  # TypeScript type definitions
│   └── api/                    # API client and related functions
├── app.html                    # Main HTML template
├── app.css                     # Global CSS styles
└── app.d.ts                    # TypeScript declarations
```

## 3. Development Workflow

### 3.1. Getting Started

1. **Install Dependencies**:

   ```bash
   npm install
   ```

2. **Run Development Server**:

   ```bash
   npm run dev
   ```

3. **Open in Browser**:

   [http://localhost:5173](http://localhost:5173)

### 3.2. Code Quality

- **Linting**: We use ESLint and Prettier to enforce a consistent code style.

  ```bash
  npm run lint
  npm run format
  ```

- **Type Checking**: We use TypeScript to catch type-related errors.

  ```bash
  npm run check
  ```

### 3.3. Testing

- **Unit Tests**: We use Vitest for unit and component testing.

  ```bash
  npm run test
  ```

## 4. Component Development

- **Naming Convention**: Use PascalCase for component names (e.g., `PrimaryButton.tsx`).
- **Props**: Define props using TypeScript interfaces for type safety.
- **Accessibility**: Ensure all components are accessible by following A11y best practices.
- **Styling**: Use TailwindCSS for styling, and avoid writing custom CSS where possible.

## 5. State Management

- **TanStack Store**: Use TanStack stores for managing global and shared state.
- **TanStack Query**: Use TanStack Query for managing server state (fetching, caching, etc.).

## 6. SEO & Performance

- **SEO**: Follow the SEO best practices outlined in the [DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md) file.
- **Performance**: Optimize images, use code splitting for large components, and monitor bundle size.

## 7. Deployment

- **Build**: Create a production-ready build with:

  ```bash
  npm run build
  ```

- **Preview**: Preview the production build locally with:

  ```bash
  npm run preview
  ```

- **Deployment**: The application is deployed using Docker and Kubernetes. Refer to the main [README.md](../README.md) for more details.
