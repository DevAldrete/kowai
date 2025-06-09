import { test, expect } from '@playwright/test';

test.describe('/api/auth/register', () => {
  const registerUrl = '/api/auth/register';

  // Mocking the Neon DB interaction or UseCase for now
  // This is a placeholder for how we might intercept and mock
  // For actual mocking, Playwright's page.route() or service worker mocking would be used.
  // For this iteration, we'll assume the endpoint can run in a 'mocked' mode if a certain header is passed,
  // or that we can swap out implementations at the server level during tests (more complex).
  // Let's simplify and assume the tests will hit a real endpoint,
  // and we will later ensure the DB part is mocked or handled.

  test('should register a new user successfully and return 201', async ({ request }) => {
    const newUser = {
      email: `testuser_${Date.now()}@example.com`, // Unique email
      password: 'Password123!',
    };

    const response = await request.post(registerUrl, {
      data: newUser,
    });

    expect(response.status()).toBe(201);
    const responseBody = await response.json();

    expect(responseBody.user).toBeDefined();
    expect(responseBody.user.email).toBe(newUser.email);
    expect(responseBody.user.id).toBeDefined();
    expect(responseBody.user.passwordHash).not.toBeDefined(); // Password hash should not be returned
    expect(responseBody.message).toBe('User registered successfully.');
  });

  test('should return 400 if email is invalid', async ({ request }) => {
    const response = await request.post(registerUrl, {
      data: {
        email: 'invalid-email',
        password: 'Password123!',
      },
    });
    expect(response.status()).toBe(400);
    const responseBody = await response.json();
    expect(responseBody.error).toBeDefined();
    // The exact error message might come from the domain/application layer
    expect(responseBody.error).toContain('Invalid email format');
  });

  test('should return 400 if password is missing', async ({ request }) => {
    const response = await request.post(registerUrl, {
      data: {
        email: 'test@example.com',
        // password missing
      },
    });
    expect(response.status()).toBe(400);
    const responseBody = await response.json();
    expect(responseBody.error).toBeDefined();
    expect(responseBody.error).toContain('Password is required'); // Or similar validation message
  });

  test('should return 400 if email is missing', async ({ request }) => {
    const response = await request.post(registerUrl, {
      data: {
        // email missing
        password: 'Password123!',
      },
    });
    expect(response.status()).toBe(400);
    const responseBody = await response.json();
    expect(responseBody.error).toBeDefined();
    expect(responseBody.error).toContain('Email is required');
  });

  test('should return 409 if email already exists', async ({ request }) => {
    const existingUser = {
      email: `existing_${Date.now()}@example.com`, // Ensure this email is unique for the test run
      password: 'Password123!',
    };

    // First, register the user
    const firstResponse = await request.post(registerUrl, { data: existingUser });
    expect(firstResponse.status()).toBe(201); // Assuming this works

    // Then, attempt to register the same user again
    const secondResponse = await request.post(registerUrl, { data: existingUser });
    expect(secondResponse.status()).toBe(409);
    const responseBody = await secondResponse.json(); // Corrected: use secondResponse.json()
    expect(responseBody.error).toBeDefined();
    expect(responseBody.error).toBe('User with this email already exists.');
  });
});
