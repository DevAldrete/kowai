import { describe, it, expect, jest, beforeEach, beforeAll, afterAll } from '@jest/globals';
import { H3Event, App } from 'h3'; // For H3Event, App types

// Import the handler and the injection functions
import routeHandler, { _setReadBodyForTest, _resetReadBodyForTest } from './register';
import { InMemoryUserRepository } from '../../../infrastructure/database/in-memory-user.repository';
import { User } from '../../../domain/entities/user.entity';

// Mock parts of the h3 event and Node.js request/response objects (remains unchanged)
const mockRequest = (method: string, body?: any, headers?: any) => ({
  method,
  url: '/api/auth/register',
  headers: headers || {},
  on: () => {},
  read: () => {},
});

const mockResponse = () => {
  const res = {
    statusCode: 200, // Default
    statusMessage: '',
    setHeader: () => {},
    end: jest.fn(),
    write: jest.fn(),
  };
  return res;
};

describe('API Route: /api/auth/register (Handler Integration Test)', () => {
  let inMemoryUserRepository: InMemoryUserRepository;
  let originalNodeEnv: string | undefined;
  const mockReadBody = jest.fn(); // Define mock function at describe scope

  beforeAll(() => {
    originalNodeEnv = process.env.NODE_ENV;
    process.env.NODE_ENV = 'test';

    // Inject the mock function into the route handler module
    _setReadBodyForTest(mockReadBody as any); // Cast as any to match H3ReadBody type if complex

    if (!(global as any).inMemoryUserRepository) {
        (global as any).inMemoryUserRepository = new InMemoryUserRepository();
    }
    inMemoryUserRepository = (global as any).inMemoryUserRepository;
  });

  afterAll(() => {
    // Reset the readBody in the route handler module to its original implementation
    _resetReadBodyForTest();
    process.env.NODE_ENV = originalNodeEnv;
    delete (global as any).inMemoryUserRepository;
  });

  beforeEach(() => {
    inMemoryUserRepository.clear();
    mockReadBody.mockReset(); // Reset the mock's state (calls, return values) before each test
  });

  const createMockEvent = (method: string, body?: any, headers?: any): H3Event => {
    const req = mockRequest(method, body, headers) as any;
    const res = mockResponse() as any;
    const event = new H3Event(req, res);
    event.context = {};
    return event;
  };

  it('should register a new user successfully and return 201', async () => {
    mockReadBody.mockResolvedValue({ email: 'test@example.com', password: 'Password123!' });
    const event = createMockEvent('POST', { email: 'test@example.com', password: 'Password123!' });

    const result = await routeHandler(event);

    expect(event.node.res.statusCode).toBe(201);
    expect(result.message).toBe('User registered successfully.');
    expect(result.user).toBeDefined();
    expect(result.user.email).toBe('test@example.com');
    expect(result.user.id).toBeDefined();
    expect(result.user.passwordHash).toBeUndefined();
  });

  it('should return 400 if email is invalid', async () => {
    mockReadBody.mockResolvedValue({ email: 'invalid-email', password: 'Password123!' });
    const event = createMockEvent('POST', { email: 'invalid-email', password: 'Password123!' });

    await expect(routeHandler(event)).rejects.toThrowError('Invalid email format.');
  });

  it('should return 400 if password is missing', async () => {
    mockReadBody.mockResolvedValue({ email: 'test@example.com' }); // Password missing
    const event = createMockEvent('POST', { email: 'test@example.com' });
    await expect(routeHandler(event)).rejects.toThrowError('Password is required and must be a string.');
  });

  it('should return 400 if email is missing', async () => {
    mockReadBody.mockResolvedValue({ password: 'Password123!' }); // Email missing
    const event = createMockEvent('POST', { password: 'Password123!' });
    await expect(routeHandler(event)).rejects.toThrowError('Email is required and must be a string.');
  });

  it('should return 409 if email already exists', async () => {
    const userData = { email: 'existing@example.com', password: 'Password123!' };
    mockReadBody.mockResolvedValue(userData);
    const event1 = createMockEvent('POST', userData);
    await routeHandler(event1);

    const event2 = createMockEvent('POST', userData);
    await expect(routeHandler(event2)).rejects.toThrowError('User with this email already exists.');
  });

  it('should return 405 if method is not POST', async () => {
    mockReadBody.mockResolvedValue({});
    const event = createMockEvent('GET');
    await expect(routeHandler(event)).rejects.toThrowError('Method Not Allowed');
  });

  it('should clear repository via x-test-clear-repo header', async () => {
    const user = User.create('clear@example.com', 'somehash');
    inMemoryUserRepository.save(user);
    expect(await inMemoryUserRepository.findByEmail('clear@example.com')).not.toBeNull();

    mockReadBody.mockResolvedValue({});
    const event = createMockEvent('POST', {}, { 'x-test-clear-repo': 'true' });
    const result = await routeHandler(event);

    expect(result.message).toBe('In-memory repository cleared.');
    expect(await inMemoryUserRepository.findByEmail('clear@example.com')).toBeNull();
  });

});
