import { PasswordService } from './password.service'; // Assuming the service will be created here

describe('PasswordService', () => {
  let passwordService: PasswordService;

  beforeEach(() => {
    passwordService = new PasswordService();
  });

  it('should be defined', () => {
    expect(passwordService).toBeDefined();
  });

  describe('hashPassword', () => {
    it('should return a hash for a given password', async () => {
      const password = 'plainPassword123';
      const hash = await passwordService.hashPassword(password);
      expect(hash).toBeDefined();
      expect(hash).not.toEqual(password);
      // Bcrypt hashes typically start with a prefix like $2a$, $2b$, or $2y$
      expect(hash).toMatch(/^\$2[aby]\$[0-9]{2}\$[./0-9A-Za-z]{53}$/);
    });
  });

  describe('comparePassword', () => {
    it('should return true for a correct password and hash', async () => {
      const password = 'plainPassword123';
      // In a real test, you might hash it first, but for isolated unit test:
      const manuallyHashedPassword = await passwordService.hashPassword(password); // Using the service itself to get a valid hash

      const isMatch = await passwordService.comparePassword(password, manuallyHashedPassword);
      expect(isMatch).toBe(true);
    });

    it('should return false for an incorrect password and hash', async () => {
      const correctPassword = 'plainPassword123';
      const incorrectPassword = 'wrongPassword';
      const hash = await passwordService.hashPassword(correctPassword);

      const isMatch = await passwordService.comparePassword(incorrectPassword, hash);
      expect(isMatch).toBe(false);
    });

    it('should return false for an invalid hash format', async () => {
      const password = 'plainPassword123';
      const invalidHash = 'notAValidBcryptHash';
      // bcrypt.compare might throw an error or return false depending on the library version and input.
      // For this test, we expect it to gracefully return false or handle the error internally if it throws.
      // If it throws, the service should catch and return false.
      await expect(passwordService.comparePassword(password, invalidHash)).resolves.toBe(false);
    });
  });
});
