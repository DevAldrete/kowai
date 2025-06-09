import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { NgFor, NgIf } from '@angular/common'; // Import NgFor, NgIf

// Import KowAI theme constants to use in styles
import { kowaiPrimary } from '../theme'; // Corrected path


@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [RouterLink, RouterLinkActive, NgFor, NgIf], // Added NgIf
  template: `
    <nav class="bg-kowai-surface shadow-lg fixed top-0 left-0 right-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <a routerLink="/" class="font-heading text-2xl text-kowai-primary hover:text-opacity-80 transition-colors">
              KowAI 👻
            </a>
          </div>
          <div class="hidden md:block">
            <div class="ml-10 flex items-baseline space-x-4">
              <a *ngFor="let link of navLinks"
                 [routerLink]="link.path"
                 routerLinkActive="active-link"
                 [routerLinkActiveOptions]="{exact: link.path === '/'}"
                 class="text-kowai-text hover:text-kowai-primary px-3 py-2 rounded-md text-sm font-medium transition-colors">
                {{ link.name }}
              </a>
            </div>
          </div>
          <!-- Mobile menu button (functional hamburger to be added later if needed) -->
          <div class="md:hidden flex items-center">
            <button (click)="toggleMobileMenu()" class="text-kowai-text hover:text-kowai-primary focus:outline-none p-2">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      <!-- Mobile menu, show/hide based on mobileMenuOpen state -->
      <div *ngIf="mobileMenuOpen" class="md:hidden">
        <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <a *ngFor="let link of navLinks"
             [routerLink]="link.path"
             routerLinkActive="active-link"
             [routerLinkActiveOptions]="{exact: link.path === '/'}"
             (click)="closeMobileMenu()"
             class="text-kowai-text hover:text-kowai-primary block px-3 py-2 rounded-md text-base font-medium transition-colors">
            {{ link.name }}
          </a>
        </div>
      </div>
    </nav>
    <div class="h-16"></div> <!-- Spacer to prevent content from being hidden behind fixed navbar -->
  `,
  styles: [`
    .active-link {
      color: ${kowaiPrimary} !important;
      border-bottom: 2px solid ${kowaiPrimary};
    }

    /* Basic styling for mobile menu button if needed, Tailwind classes are preferred */
  `]
})
export class NavbarComponent {
  navLinks = [
    { path: '/', name: 'Home' },
    { path: '/about', name: 'About' },
    { path: '/features', name: 'Features' },
    { path: '/contact', name: 'Contact' }
  ];

  mobileMenuOpen = false;

  toggleMobileMenu() {
    this.mobileMenuOpen = !this.mobileMenuOpen;
  }

  closeMobileMenu() {
    this.mobileMenuOpen = false;
  }
}
