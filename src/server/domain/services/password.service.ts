import * as bcrypt from 'bcrypt';

export class PasswordService {
  private readonly saltRounds = 10;

  async hashPassword(password: string): Promise<string> {
    const salt = await bcrypt.genSalt(this.saltRounds);
    const hash = await bcrypt.hash(password, salt);
    return hash;
  }

  async comparePassword(password: string, hash: string): Promise<boolean> {
    try {
      return await bcrypt.compare(password, hash);
    } catch (error) {
      // bcrypt.compare can throw an error if the hash is malformed,
      // for example, not a valid bcrypt hash.
      // In such cases, we consider it a non-match.
      console.error('Error comparing password:', error);
      return false;
    }
  }
}
