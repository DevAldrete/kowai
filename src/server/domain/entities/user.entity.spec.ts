import { User } from './user.entity';

describe('User Entity', () => {
  const validUserProps = {
    id: '123e4567-e89b-12d3-a456-426614174000', // example UUID
    email: 'test@example.com',
    passwordHash: 'hashedPassword',
    createdAt: new Date(),
    updatedAt: new Date(),
  };

  it('should create a user instance with valid properties', () => {
    const user = new User(
      validUserProps.id,
      validUserProps.email,
      validUserProps.passwordHash,
      validUserProps.createdAt,
      validUserProps.updatedAt
    );
    expect(user).toBeInstanceOf(User);
    expect(user.id).toEqual(validUserProps.id);
    expect(user.email).toEqual(validUserProps.email);
    expect(user.passwordHash).toEqual(validUserProps.passwordHash);
    expect(user.createdAt).toEqual(validUserProps.createdAt);
    expect(user.updatedAt).toEqual(validUserProps.updatedAt);
  });

  it('should throw an error if email is invalid', () => {
    expect(() => {
      new User(
        validUserProps.id,
        'invalid-email',
        validUserProps.passwordHash,
        validUserProps.createdAt,
        validUserProps.updatedAt
      );
    }).toThrow('Invalid email format.');
  });

  it('should throw an error if ID is not a valid UUID', () => {
    expect(() => {
      new User(
        'not-a-uuid',
        validUserProps.email,
        validUserProps.passwordHash,
        validUserProps.createdAt,
        validUserProps.updatedAt
      );
    }).toThrow('Invalid user ID format. ID must be a UUID.');
  });

  it('should allow passwordHash to be initially undefined or null for new users before hashing', () => {
    // Depending on the design, passwordHash might be set later.
    // For this test, let's assume it can be null initially.
    // If the constructor requires it, this test would need adjustment.
    const user = new User(
        validUserProps.id,
        validUserProps.email,
        null, // or undefined
        validUserProps.createdAt,
        validUserProps.updatedAt
    );
    expect(user.passwordHash).toBeNull();
  });

  // Static factory method for creating a new user (common pattern)
  describe('User.create', () => {
    it('should create a new user with a generated ID and current timestamps', () => {
      const email = 'newuser@example.com';
      const passwordHash = 'newlyHashedPassword';
      const user = User.create(email, passwordHash);

      expect(user).toBeInstanceOf(User);
      expect(user.email).toEqual(email);
      expect(user.passwordHash).toEqual(passwordHash);
      expect(user.id).toMatch(/^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/); // UUID regex
      expect(user.createdAt).toBeInstanceOf(Date);
      expect(user.updatedAt).toBeInstanceOf(Date);
      expect(user.createdAt).toEqual(user.updatedAt);
    });

    it('should throw error if email is invalid for User.create', () => {
      expect(() => {
        User.create('invalid-email', 'passwordHash');
      }).toThrow('Invalid email format.');
    });

    it('should throw error if passwordHash is empty for User.create', () => {
      expect(() => {
        User.create('valid@email.com', '');
      }).toThrow('Password hash cannot be empty.');
    });
  });

});
