import { Component } from '@angular/core';
import { RouterLink } from '@angular/router'; // Import RouterLink

@Component({
  selector: 'app-kowai-welcome',
  standalone: true,
  imports: [RouterLink], // Add RouterLink to imports
  template: `
    <div class="flex flex-col min-h-screen bg-kowai-background text-kowai-text">
      <!-- Hero Section -->
      <section class="flex-grow flex flex-col items-center justify-center text-center p-8 animate-fadeIn">
        <h1 class="text-6xl font-heading mb-4">KowAI 👻</h1>
        <p class="text-4xl font-heading mb-6">KowAI: Your Personal AI Powerhouse</p>
        <p class="text-xl mb-8 max-w-2xl">
          Take back control of your AI interactions. Host your own secure, high-performance chat interface.
        </p>
        <a routerLink="/features" class="inline-block bg-kowai-primary text-kowai-text font-bold py-3 px-6 rounded-lg hover:bg-opacity-80 transition-colors">
          Get Started
        </a>
      </section>

      <!-- Features Section -->
      <section class="py-16 bg-opacity-10 bg-kowai-primary">
        <h2 class="text-3xl font-heading text-center mb-12">Key Features</h2>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid md:grid-cols-3 gap-8">
          <!-- Feature 1 -->
          <div class="bg-kowai-background p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 animate-fadeIn" style="animation-delay: 0.2s;">
            <div class="text-4xl mb-4">🔒</div>
            <h3 class="text-2xl font-heading mb-2 text-kowai-primary">Self-Hosted & Private</h3>
            <p>Your data stays yours. Run KowAI on your own infrastructure for maximum privacy and control.</p>
          </div>
          <!-- Feature 2 -->
          <div class="bg-kowai-background p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 animate-fadeIn" style="animation-delay: 0.4s;">
            <div class="text-4xl mb-4">🔄</div>
            <h3 class="text-2xl font-heading mb-2 text-kowai-primary">Multi-Model & Provider-Agnostic</h3>
            <p>Connect to various LLMs from different providers. Switch and experiment with ease.</p>
          </div>
          <!-- Feature 3 -->
          <div class="bg-kowai-background p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 animate-fadeIn" style="animation-delay: 0.6s;">
            <div class="text-4xl mb-4">🎯</div>
            <h3 class="text-2xl font-heading mb-2 text-kowai-primary">Deep AI Personalization</h3>
            <p>Fine-tune AI behavior and create custom personas for a truly tailored experience.</p>
          </div>
          <!-- Feature 4 -->
          <div class="bg-kowai-background p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 animate-fadeIn md:col-span-1" style="animation-delay: 0.8s;">
             <div class="text-4xl mb-4">⚡️</div>
            <h3 class="text-2xl font-heading mb-2 text-kowai-primary">Blazing Fast & Responsive</h3>
            <p>Built with performance in mind, ensuring smooth interactions even on less powerful devices.</p>
          </div>
          <!-- Feature 5 -->
          <div class="bg-kowai-background p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 animate-fadeIn md:col-span-2" style="animation-delay: 1.0s;">
            <div class="text-4xl mb-4">💻</div>
            <h3 class="text-2xl font-heading mb-2 text-kowai-primary">Markdown & Code Rendering</h3>
            <p>Full support for rich text formatting, including syntax highlighting for code blocks.</p>
          </div>
        </div>
      </section>

      <!-- Footer Section -->
      <footer class="text-center p-8 text-kowai-text bg-opacity-5 bg-kowai-primary">
        <p>© 2024 KowAI. All Rights Reserved.</p>
        <div class="mt-2">
          <a href="#" class="hover:text-kowai-primary mx-2">Privacy Policy</a>
          <a href="#" class="hover:text-kowai-primary mx-2">Terms of Service</a>
        </div>
      </footer>
    </div>
  `,
  styles: [`
    /* Add any component-specific styles here if needed, though Tailwind is preferred */
    /* Minor style adjustments if Tailwind classes are not sufficient */
  `]
})
export class KowaiWelcomeComponent {}
