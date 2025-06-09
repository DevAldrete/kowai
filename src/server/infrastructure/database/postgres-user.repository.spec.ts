import { jest, describe, it, expect, beforeEach } from '@jest/globals';
import { Pool, Client } from 'pg'; // Import Pool, not PoolClient directly for mocking
import { PostgresUserRepository } from './postgres-user.repository';
import { User } from '../../domain/entities/user.entity';

// Mock the 'pg' module
jest.mock('pg', () => {
  const mockClient = {
    query: jest.fn(),
    release: jest.fn(),
  };
  const mockPool = {
    connect: jest.fn(() => Promise.resolve(mockClient)),
    query: jest.fn(), // Mock top-level pool.query as well if used directly
    end: jest.fn(() => Promise.resolve()),
  };
  return {
    Pool: jest.fn(() => mockPool),
    Client: jest.fn(() => mockClient), // If Client is used directly
  };
});

describe('PostgresUserRepository', () => {
  let userRepository: PostgresUserRepository;
  let mockPool: jest.Mocked<Pool>;
  let mockClient: jest.Mocked<any>; // Client methods are on its prototype usually

  beforeEach(() => {
    // Clear all mock implementations and call history
    jest.clearAllMocks();

    // Re-initialize the repository and mocks for each test
    // This ensures that Pool() constructor is called, returning our mockPool
    userRepository = new PostgresUserRepository();

    // The Pool constructor mock should have been called now.
    // We need to get the instance of the mockPool that was created.
    // pg.Pool is a mock constructor. mock.instances gives us instances created by it.
    mockPool = (Pool as jest.Mock).mock.instances[0] as jest.Mocked<Pool>;

    // And get the client that connect() returns.
    // We need to ensure connect is called if the repository uses it per operation.
    // For this setup, let's assume connect is called, and we get the client.
    // If the repository calls pool.connect() itself, then we get the mockClient from there.
    // If the repository calls pool.query() directly, then we use mockPool.query.
    // Let's assume it uses pool.connect() then client.query() for transactions/connection management.

    // We need to access the mockClient that 'connect' on 'mockPool' resolves to.
    // Since connect is a mock, we can check its mock implementation or return value.
    // Let's get the client from the mock setup more directly.
    mockClient = { // Re-define mockClient here as it's captured in the closure by jest.mock
        query: jest.fn(),
        release: jest.fn(),
    };
    (mockPool.connect as jest.Mock).mockResolvedValue(mockClient); // Ensure connect returns this specific mockClient
    (mockPool.query as jest.Mock).mockImplementation(mockClient.query); // If pool.query is used, it uses client.query's mock
  });

  const testUser = User.create('test@example.com', 'hashedPassword');
  // Make ID and timestamps predictable for some tests
  testUser.id = 'a1b2c3d4-e5f6-7890-1234-567890abcdef';
  testUser.createdAt = new Date('2023-01-01T00:00:00.000Z');
  testUser.updatedAt = new Date('2023-01-01T00:00:00.000Z');


  describe('save', () => {
    it('should insert a new user if they do not exist', async () => {
      // Mock findById to return null, indicating user does not exist
      mockClient.query.mockResolvedValueOnce({ rows: [], rowCount: 0 });
      // Mock insert query
      mockClient.query.mockResolvedValueOnce({ rows: [{ id: testUser.id }], rowCount: 1 });

      await userRepository.save(testUser);

      expect(mockPool.connect).toHaveBeenCalledTimes(1); // Expect a connection
      // First query: findById (SELECT)
      expect(mockClient.query).toHaveBeenNthCalledWith(1, expect.stringContaining('SELECT * FROM users WHERE id ='), [testUser.id]);
      // Second query: INSERT
      expect(mockClient.query).toHaveBeenNthCalledWith(2,
        expect.stringContaining('INSERT INTO users (id, email, password_hash, created_at, updated_at) VALUES'),
        [testUser.id, testUser.email, testUser.passwordHash, testUser.createdAt, testUser.updatedAt]
      );
      expect(mockClient.release).toHaveBeenCalledTimes(1); // Ensure client is released
    });

    it('should update an existing user', async () => {
      const updatedUser = { ...testUser, email: 'updated@example.com', updatedAt: new Date('2023-01-02T00:00:00.000Z') };
      // Mock findById to return the existing user, indicating user exists
      mockClient.query.mockResolvedValueOnce({ rows: [{...testUser, password_hash: testUser.passwordHash}], rowCount: 1 });
      // Mock update query
      mockClient.query.mockResolvedValueOnce({ rows: [{ id: updatedUser.id }], rowCount: 1 });

      await userRepository.save(updatedUser as User); // Cast needed as we didn't use User.create

      expect(mockPool.connect).toHaveBeenCalledTimes(1);
      // First query: findById (SELECT)
      expect(mockClient.query).toHaveBeenNthCalledWith(1, expect.stringContaining('SELECT * FROM users WHERE id ='), [updatedUser.id]);
      // Second query: UPDATE
      expect(mockClient.query).toHaveBeenNthCalledWith(2,
        expect.stringContaining('UPDATE users SET email ='),
        [updatedUser.email, updatedUser.passwordHash, updatedUser.updatedAt, updatedUser.id]
      );
      expect(mockClient.release).toHaveBeenCalledTimes(1);
    });
  });

  describe('findByEmail', () => {
    it('should return a user if found by email', async () => {
      const dbRow = { id: testUser.id, email: testUser.email, password_hash: testUser.passwordHash, created_at: testUser.createdAt, updated_at: testUser.updatedAt };
      mockClient.query.mockResolvedValueOnce({ rows: [dbRow], rowCount: 1 });

      const foundUser = await userRepository.findByEmail(testUser.email);

      expect(mockPool.connect).toHaveBeenCalledTimes(1);
      expect(mockClient.query).toHaveBeenCalledWith(expect.stringContaining('SELECT * FROM users WHERE email ='), [testUser.email]);
      expect(foundUser).toBeInstanceOf(User);
      expect(foundUser?.id).toEqual(testUser.id);
      expect(foundUser?.email).toEqual(testUser.email);
      expect(mockClient.release).toHaveBeenCalledTimes(1);
    });

    it('should return null if user not found by email', async () => {
      mockClient.query.mockResolvedValueOnce({ rows: [], rowCount: 0 });

      const foundUser = await userRepository.findByEmail('nonexistent@example.com');

      expect(mockClient.query).toHaveBeenCalledWith(expect.stringContaining('SELECT * FROM users WHERE email ='), ['nonexistent@example.com']);
      expect(foundUser).toBeNull();
      expect(mockClient.release).toHaveBeenCalledTimes(1);
    });
  });

  describe('findById', () => {
    it('should return a user if found by ID', async () => {
      const dbRow = { id: testUser.id, email: testUser.email, password_hash: testUser.passwordHash, created_at: testUser.createdAt, updated_at: testUser.updatedAt };
      mockClient.query.mockResolvedValueOnce({ rows: [dbRow], rowCount: 1 });

      const foundUser = await userRepository.findById(testUser.id);

      expect(mockPool.connect).toHaveBeenCalledTimes(1);
      expect(mockClient.query).toHaveBeenCalledWith(expect.stringContaining('SELECT * FROM users WHERE id ='), [testUser.id]);
      expect(foundUser).toBeInstanceOf(User);
      expect(foundUser?.id).toEqual(testUser.id);
      expect(mockClient.release).toHaveBeenCalledTimes(1);
    });

    it('should return null if user not found by ID', async () => {
      mockClient.query.mockResolvedValueOnce({ rows: [], rowCount: 0 });
      const foundUser = await userRepository.findById('nonexistent-id');
      expect(foundUser).toBeNull();
      expect(mockClient.release).toHaveBeenCalledTimes(1);
    });
  });
});
