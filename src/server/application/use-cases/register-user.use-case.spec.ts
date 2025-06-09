import { jest, describe, beforeEach, it, expect } from '@jest/globals';
import { RegisterUserUseCase } from './register-user.use-case';
import { User } from '../../domain/entities/user.entity';
import { IUserRepository } from '../../domain/repositories/user.repository';
import { PasswordService } from '../../domain/services/password.service';
import { RegisterUserDto } from '../dtos/register-user.dto';

// Mocks
const mockUserRepository: jest.Mocked<IUserRepository> = {
  save: jest.fn(),
  findByEmail: jest.fn(),
  findById: jest.fn(),
};

const mockPasswordService: jest.Mocked<PasswordService> = {
  hashPassword: jest.fn(),
  comparePassword: jest.fn(), // Not used in this use case but needed for the mock type
};

describe('RegisterUserUseCase', () => {
  let registerUserUseCase: RegisterUserUseCase;

  beforeEach(() => {
    // Reset mocks before each test
    jest.clearAllMocks();
    registerUserUseCase = new RegisterUserUseCase(mockUserRepository, mockPasswordService);
  });

  const registerDto: RegisterUserDto = {
    email: 'test@example.com',
    passwordPlainText: 'password123',
  };

  it('should successfully register a new user', async () => {
    const hashedPassword = 'hashedPassword';
    mockUserRepository.findByEmail.mockResolvedValue(null); // No existing user
    mockPasswordService.hashPassword.mockResolvedValue(hashedPassword);

    // Mock User.create to control its output for the test
    const validTestId = '123e4567-e89b-12d3-a456-426614174000'; // Use a valid UUID
    const expectedUser = new User(validTestId, registerDto.email, hashedPassword, new Date(), new Date());
    jest.spyOn(User, 'create').mockReturnValue(expectedUser);

    const result = await registerUserUseCase.execute(registerDto);

    expect(mockUserRepository.findByEmail).toHaveBeenCalledWith(registerDto.email);
    expect(mockPasswordService.hashPassword).toHaveBeenCalledWith(registerDto.passwordPlainText);
    expect(User.create).toHaveBeenCalledWith(registerDto.email, hashedPassword);
    expect(mockUserRepository.save).toHaveBeenCalledWith(expectedUser);
    expect(result).toEqual(expectedUser);
  });

  it('should throw an error if user already exists', async () => {
    const existingUser = User.create(registerDto.email, 'someHash');
    mockUserRepository.findByEmail.mockResolvedValue(existingUser);

    await expect(registerUserUseCase.execute(registerDto)).rejects.toThrow('User with this email already exists.');

    expect(mockUserRepository.findByEmail).toHaveBeenCalledWith(registerDto.email);
    expect(mockPasswordService.hashPassword).not.toHaveBeenCalled();
    expect(mockUserRepository.save).not.toHaveBeenCalled();
  });

  it('should throw an error if email is invalid (delegated to User entity)', async () => {
    // This test relies on User.create throwing an error for invalid email
    // which is already tested in user.entity.spec.ts.
    // Here, we ensure the use case doesn't hide or incorrectly handle that.
    const invalidEmailDto: RegisterUserDto = { ...registerDto, email: 'invalid' };
    mockUserRepository.findByEmail.mockResolvedValue(null);
    mockPasswordService.hashPassword.mockResolvedValue('hashedPassword');

    // User.create will throw, so we expect the use case to propagate that.
    // We need to mock User.create to actually throw the expected error.
    jest.spyOn(User, 'create').mockImplementation(() => {
      throw new Error('Invalid email format.');
    });

    await expect(registerUserUseCase.execute(invalidEmailDto)).rejects.toThrow('Invalid email format.');
  });

  it('should throw an error if password hashing fails', async () => {
    mockUserRepository.findByEmail.mockResolvedValue(null);
    mockPasswordService.hashPassword.mockRejectedValue(new Error('Hashing failed'));

    await expect(registerUserUseCase.execute(registerDto)).rejects.toThrow('Hashing failed');
    expect(mockPasswordService.hashPassword).toHaveBeenCalledWith(registerDto.passwordPlainText);
  });

  it('should throw an error if saving user fails', async () => {
    const hashedPassword = 'hashedPassword';
    mockUserRepository.findByEmail.mockResolvedValue(null);
    mockPasswordService.hashPassword.mockResolvedValue(hashedPassword);

    const validTestIdForSave = '223e4567-e89b-12d3-a456-426614174001'; // Use a different valid UUID
    const userToSave = new User(validTestIdForSave, registerDto.email, hashedPassword, new Date(), new Date());
    jest.spyOn(User, 'create').mockReturnValue(userToSave);

    mockUserRepository.save.mockRejectedValue(new Error('Database save failed'));

    await expect(registerUserUseCase.execute(registerDto)).rejects.toThrow('Database save failed');
    expect(mockUserRepository.save).toHaveBeenCalledWith(userToSave);
  });
});
