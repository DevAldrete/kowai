import { User } from '../../domain/entities/user.entity';
import { IUserRepository } from '../../domain/repositories/user.repository';
import { PasswordService } from '../../domain/services/password.service';
import { RegisterUserDto } from '../dtos/register-user.dto';

export class RegisterUserUseCase {
  constructor(
    private readonly userRepository: IUserRepository,
    private readonly passwordService: PasswordService
  ) {}

  async execute(registerUserDto: RegisterUserDto): Promise<User> {
    const { email, passwordPlainText } = registerUserDto;

    // Check if user already exists
    const existingUser = await this.userRepository.findByEmail(email);
    if (existingUser) {
      throw new Error('User with this email already exists.');
    }

    // Hash the password
    let hashedPassword: string;
    try {
      hashedPassword = await this.passwordService.hashPassword(passwordPlainText);
    } catch (error) {
      // Assuming hashPassword might throw if underlying bcrypt fails unexpectedly
      const message = error instanceof Error ? error.message : 'Error hashing password.';
      throw new Error(message);
    }

    // Create new user entity
    // This step can throw an error if email is invalid or passwordHash is empty (validated by User.create)
    const newUser = User.create(email, hashedPassword);

    // Save the new user
    try {
      await this.userRepository.save(newUser);
    } catch (error) {
      // Assuming save might throw if underlying database operation fails
      const message = error instanceof Error ? error.message : 'Error saving user to database.';
      throw new Error(message);
    }

    return newUser;
  }
}
