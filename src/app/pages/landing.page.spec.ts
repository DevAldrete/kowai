import { TestBed, ComponentFixture } from '@angular/core/testing';
import { LandingPageComponent } from './landing.page';
import { NO_ERRORS_SCHEMA } from '@angular/core'; // To avoid issues with unknown elements if any

// Vitest imports - assuming a Vitest environment based on project context
// If using Jest or Karma, these would be slightly different
import { describe, it, expect, beforeEach } from 'vitest';

describe('LandingPageComponent', () => {
  let component: LandingPageComponent;
  let fixture: ComponentFixture<LandingPageComponent>;
  let nativeElement: HTMLElement;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LandingPageComponent], // For standalone components, they are imported
      // declarations: [LandingPageComponent], // Not needed for standalone components in imports array
      schemas: [NO_ERRORS_SCHEMA] // Useful if template has other custom components not mocked/imported
    }).compileComponents();

    fixture = TestBed.createComponent(LandingPageComponent);
    component = fixture.componentInstance;
    nativeElement = fixture.nativeElement;
    fixture.detectChanges(); // Trigger initial data binding
  });

  it('should create the component successfully', () => {
    expect(component).toBeTruthy();
  });

  it('should render the hero section main heading', () => {
    const heroHeading = nativeElement.querySelector('h1');
    expect(heroHeading).toBeTruthy();
    expect(heroHeading?.textContent).toContain('Welcome to Our Awesome Product!');
  });

  it('should render the features section title', () => {
    // The features section title is the second h2. A more robust selector could be a class or ID.
    // For now, we'll find it by text, assuming it's distinct enough or by structure.
    const sectionTitles = nativeElement.querySelectorAll('h2');
    let featuresTitle: Element | undefined;
    sectionTitles.forEach(title => {
      if (title.textContent?.includes('Why Choose Us?')) {
        featuresTitle = title;
      }
    });
    expect(featuresTitle).toBeTruthy();
    expect(featuresTitle?.textContent).toContain('Why Choose Us?');
  });

  it('should render the call-to-action section button', () => {
    const buttons = nativeElement.querySelectorAll('button');
    let ctaButton: HTMLButtonElement | undefined;
    buttons.forEach(button => {
      if (button.textContent?.includes('Sign Up Now')) {
        ctaButton = button;
      }
    });
    expect(ctaButton).toBeTruthy();
    expect(ctaButton?.textContent).toContain('Sign Up Now');
  });
});
