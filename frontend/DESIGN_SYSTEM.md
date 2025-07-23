# KowAI Design System

<div align="center">

![KowAI Design System](https://img.shields.io/badge/Design_System-KowAI_Frontend-4A148C?style=for-the-badge&logo=figma&logoColor=white)

*A comprehensive guide to the visual language, components, and user experience principles for the KowAI application.*

</div>

## 1. Design Philosophy

Our design philosophy is centered around creating an interface that is **minimalist, playful, and futuristic**. We aim to blend a clean, modern aesthetic with engaging, game-inspired elements to make the user experience both intuitive and delightful.

-   **Clarity First**: The interface should be clean and uncluttered, ensuring that users can easily navigate and interact with the application.
-   **Playful Engagement**: Incorporate subtle animations, visual effects, and micro-interactions to make the experience enjoyable and memorable.
-   **Futuristic Aesthetic**: Leverage dark themes, glass morphism, and neon accents to create a cutting-edge, tech-forward look and feel.
-   **Accessibility by Design**: Ensure the application is usable by everyone, regardless of their abilities, by following best practices for accessibility.

## 2. Color Palette

The color palette is designed to be dark, vibrant, and sophisticated, creating a high-contrast and visually appealing experience.

### Primary Colors

| Color          | Hex       | Usage                               |
| :------------- | :-------- | :---------------------------------- |
| Deep Purple    | `#4A148C` | Primary brand color, CTAs, highlights |
| Dark Gray      | `#1A1A1A` | Main background color               |

### Accent Colors

| Color          | Hex       | Usage                                     |
| :------------- | :-------- | :---------------------------------------- |
| Electric Blue  | `#00B4D8` | Interactive elements, links, focus states |
| Magenta        | `#FF00FF` | Secondary accents, gradients, highlights  |
| Neon Green     | `#39FF14` | Success states, positive feedback       |
| Cyber Yellow   | `#FFD700` | Warnings, notifications, attention      |

### Semantic Colors

| Color   | Hex       | Usage                               |
| :------ | :-------- | :---------------------------------- |
| Success | `#10B981` | Success messages, validation        |
| Warning | `#F59E0B` | Warning messages, pending states    |
| Error   | `#EF4444` | Error messages, destructive actions |
| Info    | `#3B82F6` | Informational tooltips, helpers     |

### Glass Morphism

| Name           | Value                       | Usage                               |
| :------------- | :-------------------------- | :---------------------------------- |
| Glass BG       | `rgba(26, 26, 26, 0.8)`     | Background for cards and modals     |
| Glass Border   | `rgba(255, 255, 255, 0.1)`  | Borders for glass elements          |
| Glass Shadow   | `rgba(0, 0, 0, 0.3)`        | Subtle shadows for depth            |

### Gradients

| Name              | Value                                                 | Usage                                     |
| :---------------- | :---------------------------------------------------- | :---------------------------------------- |
| Gradient Primary  | `linear-gradient(135deg, #4A148C 0%, #1A1A1A 100%)`    | Hero sections, primary backgrounds        |
| Gradient Accent   | `linear-gradient(45deg, #00B4D8 0%, #FF00FF 100%)`     | Accent backgrounds, decorative elements   |
| Gradient Spotlight| `radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%)` | Hover effects, interactive highlights |

## 3. Typography

Our typography system is designed for clarity, readability, and a modern aesthetic.

### Font Families

| Name         | Family                                           | Usage                 |
| :----------- | :----------------------------------------------- | :-------------------- |
| Font Primary | `'Inter', sans-serif`                            | Body text, UI elements|
| Font Mono    | `'JetBrains Mono', monospace`                    | Code snippets, data   |
| Font Display | `'Space Grotesk', sans-serif`                    | Headings, titles      |

### Font Scale & Weights

| Size      | `rem`  | `px` | Weight(s)                               |
| :-------- | :----- | :--- | :-------------------------------------- |
| `text-xs` | 0.75   | 12   | Normal                                  |
| `text-sm` | 0.875  | 14   | Normal, Medium                          |
| `text-base`| 1      | 16   | Normal, Medium, Semibold                |
| `text-lg` | 1.125  | 18   | Semibold, Bold                          |
| `text-xl` | 1.25   | 20   | Bold                                    |
| `text-2xl`| 1.5    | 24   | Bold, Black                             |
| `text-3xl`| 1.875  | 30   | Black                                   |
| `text-4xl`| 2.25   | 36   | Black                                   |
| `text-5xl`| 3      | 48   | Black                                   |

## 4. Visual Effects

### Glass Morphism

Apply to cards, modals, and sidebars to create a sense of depth and transparency.

```css
.glass-card {
  background: rgba(26, 26, 26, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  border-radius: 16px;
}
```

### Spotlight Effect

Use on interactive elements to draw attention on hover.

```css
.spotlight-hover {
  position: relative;
  overflow: hidden;
}
.spotlight-hover:hover::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  opacity: 1;
  transition: opacity 0.3s ease;
}
```

### Grain Texture

Apply a subtle grain overlay to large background areas to add texture and depth.

```css
.grain-texture::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,..."); /* SVG noise */
  opacity: 0.15;
  pointer-events: none;
  mix-blend-mode: overlay;
}
```

### Neon Highlights

Use for primary buttons and important interactive elements to create a vibrant glow.

```css
.neon-glow {
  box-shadow: 0 0 5px #00B4D8, 0 0 10px #00B4D8, 0 0 15px #00B4D8;
  animation: neon-pulse 2s ease-in-out infinite alternate;
}
```

## 5. Animation System

Animations should be smooth, purposeful, and enhance the user experience.

-   **Text Animations**: Use typewriter and glitch effects for headings and taglines.
-   **UI Animations**: Use fade-in-up for page loads and new elements.
-   **Micro-interactions**: Use subtle animations for button clicks, toggles, and other interactive elements.

## 6. Component States

Ensure all interactive components have distinct visual states.

-   **Idle**: The default state of the component.
-   **Hover**: When the user's cursor is over the component.
-   **Active/Pressed**: When the user clicks or taps the component.
-   **Focus**: When the component is selected via keyboard navigation.
-   **Disabled**: When the component is not interactive.

## 7. Layout & Grid

-   **Grid System**: Use a 12-column flexible grid for consistent and responsive layouts.
-   **Spacing**: Use a base-8 spacing system (8px, 16px, 24px, etc.) for margins, padding, and positioning.

## 8. Iconography

-   **Style**: Use a consistent set of line-based icons with a modern, minimalist style.
-   **Library**: Prefer a single icon library (e.g., Lucide, Feather Icons) for consistency.
-   **Usage**: Icons should be clear, simple, and easily recognizable.

## 9. SEO Best Practices

-   **Meta Tags**: Ensure all pages have unique and descriptive `title`, `description`, and `keywords`.
-   **Semantic HTML**: Use appropriate HTML5 tags (`<main>`, `<nav>`, `<article>`, etc.).
-   **Performance**: Optimize images, lazy load non-critical assets, and minimize bundle size.
-   **Accessibility**: Follow A11y guidelines to improve search engine ranking.

## 10. Accessibility (A11y)

-   **Keyboard Navigation**: All interactive elements must be accessible and operable via keyboard.
-   **ARIA Roles**: Use appropriate ARIA roles and attributes to enhance screen reader compatibility.
-   **Color Contrast**: Ensure text and interactive elements meet WCAG AA contrast ratios.
-   **Focus Management**: Implement logical focus order and visible focus states.

## 11. Voice & Tone

-   **Clarity**: Use clear, concise, and straightforward language.
-   **Playfulness**: Inject a touch of personality and fun into the copy.
-   **Helpfulness**: Provide helpful and informative messages, especially for errors and empty states.
