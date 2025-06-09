import { Component } from '@angular/core';
import { NavbarComponent } from '../components/navbar/navbar.component'; // Import NavbarComponent

@Component({
  selector: 'app-features-page',
  standalone: true,
  imports: [NavbarComponent], // Add NavbarComponent to imports
  template: `
    <app-navbar></app-navbar> <!-- Add navbar selector -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-kowai-text min-h-screen">
      <h1 class="font-heading text-3xl md:text-4xl mb-12 text-center text-kowai-primary animate-fadeIn">
        Explore KowAI's Powerful Features
      </h1>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- Feature Card 1 -->
        <div class="bg-kowai-surface p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 animate-fadeIn" style="animation-delay: 0.1s;">
          <div class="text-4xl mb-4 text-kowai-accent">🔒</div>
          <h3 class="font-heading text-xl mb-3 text-kowai-secondary">Self-Hosted & Private</h3>
          <p class="text-base leading-relaxed">
            Run KowAI on your own infrastructure. Your conversations and API keys are yours alone.
            No tracking, no third-party data access.
          </p>
        </div>

        <!-- Feature Card 2 -->
        <div class="bg-kowai-surface p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 animate-fadeIn" style="animation-delay: 0.2s;">
          <div class="text-4xl mb-4 text-kowai-accent">🔄</div>
          <h3 class="font-heading text-xl mb-3 text-kowai-secondary">Multi-Model & Provider-Agnostic</h3>
          <p class="text-base leading-relaxed">
            Connect to OpenAI, Anthropic, Google, Groq, or local models via Ollama.
            Switch models on the fly.
          </p>
        </div>

        <!-- Feature Card 3 -->
        <div class="bg-kowai-surface p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 animate-fadeIn" style="animation-delay: 0.3s;">
          <div class="text-4xl mb-4 text-kowai-accent">🎯</div>
          <h3 class="font-heading text-xl mb-3 text-kowai-secondary">Deep AI Personalization</h3>
          <p class="text-base leading-relaxed">
            Control core model parameters. Craft unique AI 'Personas' with custom system
            instructions and save them.
          </p>
        </div>

        <!-- Feature Card 4 -->
        <div class="bg-kowai-surface p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 animate-fadeIn" style="animation-delay: 0.4s;">
          <div class="text-4xl mb-4 text-kowai-accent">⚡️</div>
          <h3 class="font-heading text-xl mb-3 text-kowai-secondary">Blazing Fast & Responsive</h3>
          <p class="text-base leading-relaxed">
            Built with a Go backend and Angular frontend for real-time, streamed responses.
            Experience the speed.
          </p>
        </div>

        <!-- Feature Card 5 -->
        <div class="bg-kowai-surface p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 animate-fadeIn" style="animation-delay: 0.5s;">
          <div class="text-4xl mb-4 text-kowai-accent">💻</div>
          <h3 class="font-heading text-xl mb-3 text-kowai-secondary">Markdown & Code Rendering</h3>
          <p class="text-base leading-relaxed">
            Beautifully formatted responses with syntax highlighting for code blocks.
            Perfect for developers.
          </p>
        </div>

        <!-- Feature Card 6 -->
        <div class="bg-kowai-surface p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 animate-fadeIn" style="animation-delay: 0.6s;">
          <div class="text-4xl mb-4 text-kowai-accent">🏛️</div>
          <h3 class="font-heading text-xl mb-3 text-kowai-secondary">Clean Architecture</h3>
          <p class="text-base leading-relaxed">
            Hexagonal backend architecture ensures a maintainable, testable, and
            extensible codebase for future growth.
          </p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    /* Component-specific styles can go here if needed. */
  `]
})
export class FeaturesPageComponent {}
