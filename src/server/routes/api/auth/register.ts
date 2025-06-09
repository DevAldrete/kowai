import { defineEventHandler, readBody as actualReadBody, createError } from 'h3';
import { RegisterUserUseCase } from '../../../application/use-cases/register-user.use-case';
import { PasswordService } from '../../../domain/services/password.service';
import { InMemoryUserRepository } from '../../../infrastructure/database/in-memory-user.repository';
import { IUserRepository } from '../../../domain/repositories/user.repository';
import { User } from '../../../domain/entities/user.entity';

let currentReadBody = actualReadBody;

// Test-only export for injecting readBody mock
export function _setReadBodyForTest(mockReadBody: typeof actualReadBody): void {
  if (process.env.NODE_ENV === 'test') {
    currentReadBody = mockReadBody;
  } else {
    console.warn('_setReadBodyForTest should only be called in test environment.');
  }
}

// Test-only export for resetting readBody mock
export function _resetReadBodyForTest(): void {
  if (process.env.NODE_ENV === 'test') {
    currentReadBody = actualReadBody;
  } else {
    console.warn('_resetReadBodyForTest should only be called in test environment.');
  }
}

// A simple mechanism to get the repository (remains unchanged from before).
function getUserRepository(): IUserRepository {
  if (process.env.USE_IN_MEMORY_DB === 'true' || process.env.NODE_ENV === 'test') {
    if (!(global as any).inMemoryUserRepository) {
        (global as any).inMemoryUserRepository = new InMemoryUserRepository();
    }
    return (global as any).inMemoryUserRepository;
  }
  console.warn("WARN: Using InMemoryUserRepository for /api/auth/register. Ensure this is intended for production if NODE_ENV is not 'test'.");
  if (!(global as any).inMemoryUserRepository) {
      (global as any).inMemoryUserRepository = new InMemoryUserRepository();
  }
  return (global as any).inMemoryUserRepository;
}

const passwordService = new PasswordService();
const userRepository = getUserRepository();
const registerUserUseCase = new RegisterUserUseCase(userRepository, passwordService);

export default defineEventHandler(async (event) => {
  // Handle x-test-clear-repo first, only in test environment
  if (
    process.env.NODE_ENV === 'test' &&
    event.node.req.headers['x-test-clear-repo'] === 'true' &&
    userRepository instanceof InMemoryUserRepository // userRepository is from outer scope
  ) {
    (userRepository as InMemoryUserRepository).clear();
    return { message: 'In-memory repository cleared.' };
  }

  if (event.node.req.method !== 'POST') {
    throw createError({ statusCode: 405, statusMessage: 'Method Not Allowed' });
  }

  const body = await currentReadBody(event); // Use the injectable currentReadBody

  // Ensure body is not null or undefined before destructuring
  if (!body) {
    throw createError({ statusCode: 400, statusMessage: 'Request body is missing.' });
  }

  const { email, password } = body;

  if (!email || typeof email !== 'string') {
    throw createError({ statusCode: 400, statusMessage: 'Email is required and must be a string.' });
  }
  if (!password || typeof password !== 'string') {
    throw createError({ statusCode: 400, statusMessage: 'Password is required and must be a string.' });
  }

  try {
    const user = await registerUserUseCase.execute({ email, passwordPlainText: password });

    const userResponse = {
      id: user.id,
      email: user.email,
      createdAt: user.createdAt,
      updatedAt: user.updatedAt,
    };

    event.node.res.statusCode = 201; // Created
    return {
      message: 'User registered successfully.',
      user: userResponse,
    };
  } catch (error: any) {
    if (error.message.includes('User with this email already exists')) {
      throw createError({ statusCode: 409, statusMessage: error.message });
    }
    if (error.message.includes('Invalid email format') || error.message.includes('Password hash cannot be empty')) {
      throw createError({ statusCode: 400, statusMessage: error.message });
    }
    console.error('Registration Error:', error);
    throw createError({ statusCode: 500, statusMessage: 'An unexpected error occurred.' });
  }
});
