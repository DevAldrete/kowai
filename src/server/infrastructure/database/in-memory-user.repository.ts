import { User } from '../../domain/entities/user.entity';
import { IUserRepository } from '../../domain/repositories/user.repository';

export class InMemoryUserRepository implements IUserRepository {
  private users: User[] = [];

  async save(user: User): Promise<void> {
    // Simulate immutability: find and replace or add
    const existingUserIndex = this.users.findIndex(u => u.id === user.id);
    if (existingUserIndex > -1) {
      this.users[existingUserIndex] = user;
    } else {
      this.users.push(user);
    }
    // In a real DB, this might throw an error if something goes wrong.
    // For in-memory, we assume success.
    return Promise.resolve();
  }

  async findByEmail(email: string): Promise<User | null> {
    const user = this.users.find(u => u.email === email);
    return Promise.resolve(user || null);
  }

  async findById(id: string): Promise<User | null> {
    const user = this.users.find(u => u.id === id);
    return Promise.resolve(user || null);
  }

  // Helper for clearing data in tests if needed
  clear(): void {
    this.users = [];
  }
}
