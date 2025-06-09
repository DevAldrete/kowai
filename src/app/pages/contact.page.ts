import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms'; // Import FormsModule for ngModel
import { NavbarComponent } from '../components/navbar/navbar.component'; // Import NavbarComponent
import { NgIf } from '@angular/common'; // Import NgIf for *ngIf

@Component({
  selector: 'app-contact-page',
  standalone: true,
  imports: [FormsModule, NavbarComponent, NgIf], // Add NavbarComponent and NgIf to imports
  template: `
    <app-navbar></app-navbar> <!-- Add navbar selector -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-kowai-text min-h-screen">
      <h1 class="font-heading text-3xl md:text-4xl mb-6 text-center text-kowai-primary animate-fadeIn">
        Get In Touch
      </h1>
      <p class="text-lg md:text-xl text-center mb-10 animate-fadeIn" style="animation-delay: 0.2s;">
        Have questions, feedback, or want to contribute? We'd love to hear from you!
      </p>

      <div class="max-w-3xl mx-auto">
        <section class="animate-fadeIn mb-12" style="animation-delay: 0.4s;">
          <h2 class="font-heading text-2xl mb-4 text-kowai-secondary">Contact Channels</h2>
          <div class="space-y-3 text-lg">
            <p>
              <strong>Email:</strong>
              <a href="mailto:contact@kowai.host" class="text-kowai-primary hover:underline ml-2">
                contact@kowai.host
              </a>
            </p>
            <p>
              <strong>Community Discord:</strong>
              <a href="https://discord.gg/your-server-link" target="_blank" rel="noopener noreferrer" class="text-kowai-primary hover:underline ml-2">
                Join the KowAI Discord Server
              </a>
              (Link to be updated)
            </p>
            <p>
              <strong>GitHub Issues:</strong>
              <a href="https://github.com/your-repo/issues" target="_blank" rel="noopener noreferrer" class="text-kowai-primary hover:underline ml-2">
                Report a Bug or Request a Feature
              </a>
              (Link to be updated)
            </p>
          </div>
        </section>

        <section class="animate-fadeIn" style="animation-delay: 0.6s;">
          <h2 class="font-heading text-2xl mb-6 text-kowai-secondary">Send us a Message</h2>
          <form (submit)="submitForm($event)" class="space-y-6">
            <div>
              <label for="name" class="block text-sm font-medium text-kowai-text/70 mb-1">Full Name</label>
              <input type="text" name="name" id="name" [(ngModel)]="formData.name" required
                     class="mt-1 block w-full px-3 py-2 bg-kowai-surface border border-kowai-primary/50 rounded-md shadow-sm focus:outline-none focus:ring-kowai-primary focus:border-kowai-primary sm:text-sm text-kowai-text placeholder-kowai-text/70"
                     placeholder="Your Name">
            </div>
            <div>
              <label for="email" class="block text-sm font-medium text-kowai-text/70 mb-1">Email Address</label>
              <input type="email" name="email" id="email" [(ngModel)]="formData.email" required
                     class="mt-1 block w-full px-3 py-2 bg-kowai-surface border border-kowai-primary/50 rounded-md shadow-sm focus:outline-none focus:ring-kowai-primary focus:border-kowai-primary sm:text-sm text-kowai-text placeholder-kowai-text/70"
                     placeholder="you@example.com">
            </div>
            <div>
              <label for="message" class="block text-sm font-medium text-kowai-text/70 mb-1">Message</label>
              <textarea name="message" id="message" rows="4" [(ngModel)]="formData.message" required
                        class="mt-1 block w-full px-3 py-2 bg-kowai-surface border border-kowai-primary/50 rounded-md shadow-sm focus:outline-none focus:ring-kowai-primary focus:border-kowai-primary sm:text-sm text-kowai-text placeholder-kowai-text/70"
                        placeholder="Your message..."></textarea>
            </div>
            <div>
              <button type="submit"
                      class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-kowai-text bg-kowai-primary hover:bg-opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-kowai-primary transition-colors">
                Send Message
              </button>
            </div>
          </form>
          <p *ngIf="formSubmitted" class="mt-4 text-center text-kowai-success animate-fadeIn">
            Thank you for your message! We'll get back to you soon.
          </p>
        </section>
      </div>
    </div>
  `,
  styles: [`
    /* Component-specific styles can go here if needed. */
  `]
})
export class ContactPageComponent {
  formData = {
    name: '',
    email: '',
    message: ''
  };
  formSubmitted = false;

  submitForm(event: Event) {
    event.preventDefault(); // Prevent actual form submission
    console.log('Form data:', this.formData);
    this.formSubmitted = true;
    // Here you would typically send the data to a backend service
    // For now, we'll just log it and show a success message
    setTimeout(() => {
      this.formSubmitted = false; // Hide message after a few seconds
      this.formData = { name: '', email: '', message: '' }; // Reset form
    }, 5000);
  }
}
