import { Component } from '@angular/core';

import { LandingPageComponent } from './landing.page';

@Component({
  selector: 'app-home',
  imports: [LandingPageComponent],
  template: `
     <app-landing-page></app-landing-page>
  `,
})
export default class HomeComponent {
}
