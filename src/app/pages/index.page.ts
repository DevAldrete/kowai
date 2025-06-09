import { Component } from '@angular/core';
import { KowaiWelcomeComponent } from './kowai-welcome';
import { NavbarComponent } from '../components/navbar/navbar.component'; // Import NavbarComponent

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [NavbarComponent, KowaiWelcomeComponent], // Add NavbarComponent to imports
  template: `
     <app-navbar></app-navbar> <!-- Add navbar selector -->
     <app-kowai-welcome/>
  `,
})
export default class HomeComponent {
}
