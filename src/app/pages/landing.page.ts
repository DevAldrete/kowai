import { Component } from '@angular/core';

@Component({
  selector: 'app-landing-page',
  template: `
    <!-- Hero Section -->
    <div class="bg-gray-900 text-center py-16 px-6">
      <h1 class="text-5xl font-bold text-white mb-6">
        Welcome to Our Awesome Product!
      </h1>
      <p class="text-xl text-gray-300 mb-8">
        Discover how our solution can revolutionize your workflow and boost productivity.
      </p>
      <button class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg text-lg">
        Get Started Today
      </button>
    </div>

    <!-- Features Section -->
    <div class="py-16 px-6">
      <h2 class="text-4xl font-bold text-gray-800 text-center mb-12">
        Why Choose Us?
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        <!-- Feature 1 -->
        <div class="bg-white p-6 rounded-lg shadow-lg text-center">
          <div class="text-blue-500 text-4xl mb-4">ICON_PLACEHOLDER_1</div>
          <h3 class="text-2xl font-bold text-gray-700 mb-3">Innovative Features</h3>
          <p class="text-gray-600">
            Our product is packed with cutting-edge features designed for modern needs.
          </p>
        </div>
        <!-- Feature 2 -->
        <div class="bg-white p-6 rounded-lg shadow-lg text-center">
          <div class="text-blue-500 text-4xl mb-4">ICON_PLACEHOLDER_2</div>
          <h3 class="text-2xl font-bold text-gray-700 mb-3">User-Friendly Interface</h3>
          <p class="text-gray-600">
            Experience a seamless and intuitive interface that requires minimal learning.
          </p>
        </div>
        <!-- Feature 3 -->
        <div class="bg-white p-6 rounded-lg shadow-lg text-center">
          <div class="text-blue-500 text-4xl mb-4">ICON_PLACEHOLDER_3</div>
          <h3 class="text-2xl font-bold text-gray-700 mb-3">Reliable Support</h3>
          <p class="text-gray-600">
            Get access to our dedicated support team whenever you need assistance.
          </p>
        </div>
      </div>
    </div>

    <!-- Call-to-Action Section -->
    <div class="bg-gray-200 py-16 px-6 text-center">
      <h2 class="text-3xl font-bold text-gray-800 mb-6">
        Ready to Take the Next Step?
      </h2>
      <p class="text-lg text-gray-700 mb-8">
        Join thousands of satisfied customers and transform your business.
      </p>
      <button class="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-8 rounded-lg text-lg">
        Sign Up Now
      </button>
    </div>
  `,
  styles: []
})
export class LandingPageComponent { }
