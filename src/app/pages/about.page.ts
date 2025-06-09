import { Component } from '@angular/core';
import { NavbarComponent } from '../components/navbar/navbar.component'; // Import NavbarComponent

@Component({
  selector: 'app-about-page',
  standalone: true,
  imports: [NavbarComponent], // Add NavbarComponent to imports
  template: `
    <app-navbar></app-navbar> <!-- Add navbar selector -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-kowai-text min-h-screen">
      <h1 class="font-heading text-3xl md:text-4xl mb-10 text-center text-kowai-primary animate-fadeIn">
        About KowAI 👻
      </h1>

      <section class="animate-fadeIn" style="animation-delay: 0.2s;">
        <h2 class="font-heading text-2xl md:text-3xl mb-4 text-kowai-secondary">Our Mission</h2>
        <p class="text-lg md:text-xl leading-relaxed">
          KowAI is dedicated to providing users with a secure, private, and powerful AI chat experience.
          We believe in empowering users to control their data and customize their AI interactions to
          build their very own, scary-good AI assistants.
        </p>
      </section>

      <section class="animate-fadeIn mt-12" style="animation-delay: 0.4s;">
        <h2 class="font-heading text-2xl md:text-3xl mb-4 text-kowai-secondary">Our Story</h2>
        <p class="text-lg md:text-xl leading-relaxed">
          Founded on the principles of data sovereignty and AI accessibility, KowAI started as a project
          to demystify AI and put powerful tools directly into the hands of power-users. We envision a
          future where everyone can have personalized AI agents tailored to their unique needs, without
          compromising on privacy. Our journey is fueled by a passion for open-source innovation and
          a commitment to building a truly user-centric AI interface.
        </p>
      </section>

      <section class="animate-fadeIn mt-12" style="animation-delay: 0.6s;">
        <h2 class="font-heading text-2xl md:text-3xl mb-4 text-kowai-secondary">Why "KowAI"?</h2>
        <p class="text-lg md:text-xl leading-relaxed">
          The name "KowAI" (怖い - Japanese for "scary" or "eerie") is a playful nod to the
          sometimes intimidating power of AI. We aim to make this power approachable and controllable,
          turning the "scary" into "scary-good" for our users. The ghost emoji 👻 is our friendly mascot,
          representing the helpful (and perhaps a little mischievous) spirit of your personal AI.
        </p>
      </section>
    </div>
  `,
  styles: [`
    /* Component-specific styles can go here if needed. */
  `]
})
export class AboutPageComponent {}
