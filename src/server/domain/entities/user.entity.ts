import { v4 as uuidv4, validate as validateUUID } from 'uuid';

export class User {
  public readonly id: string;
  public readonly email: string;
  public readonly passwordHash: string | null; // Allow null as per test
  public readonly createdAt: Date;
  public readonly updatedAt: Date;

  constructor(
    id: string,
    email: string,
    passwordHash: string | null,
    createdAt: Date,
    updatedAt: Date
  ) {
    if (!User.isValidEmail(email)) {
      throw new Error('Invalid email format.');
    }
    if (!validateUUID(id)) {
      throw new Error('Invalid user ID format. ID must be a UUID.');
    }

    this.id = id;
    this.email = email;
    this.passwordHash = passwordHash;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
  }

  private static isValidEmail(email: string): boolean {
    // Basic email validation regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  public static create(email: string, passwordHash: string): User {
    if (!User.isValidEmail(email)) {
      throw new Error('Invalid email format.');
    }
    if (!passwordHash) { // Check for empty, null, or undefined
      throw new Error('Password hash cannot be empty.');
    }

    const id = uuidv4();
    const now = new Date();
    return new User(id, email, passwordHash, now, now);
  }
}
