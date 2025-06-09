export default {
  preset: 'ts-jest/presets/default-esm',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  moduleFileExtensions: ['ts', 'js', 'json', 'node'],
  transform: {
    // '^.+\\.tsx?$': ['ts-jest', { // ts-jest/presets/default-esm should configure this
    //   tsconfig: '<rootDir>/tsconfig.spec.json',
    //   useESM: true,
    // }],
    '^.+\\.m?[tj]sx?$': ['ts-jest', { // More generic to catch .ts, .tsx, .mts, .mtsx, .js, .jsx, .mjs, .mjsx
        tsconfig: '<rootDir>/tsconfig.spec.json',
        useESM: true,
    }],
  },
  transformIgnorePatterns: [
    "/node_modules/(?!(@angular|@analogjs|rxjs|tslib)/)" // Added tslib as it's often needed too
  ],
  testMatch: [
    '**/__tests__/**/*.+(ts|js)',
    '**/?(*.)+(spec|test).+(ts|js)',
  ],
  setupFilesAfterEnv: ['<rootDir>/src/test-setup.ts'],
  // AnalogJS might require specific module mappings or configurations.
  // This is a basic setup and might need adjustments.
  moduleNameMapper: {
    // Add any necessary module aliases here, for example:
    // '^@app/(.*)$': '<rootDir>/src/app/$1',
    // '^@server/(.*)$': '<rootDir>/src/server/$1',
    // If using useESM, Jest might try to resolve .js extensions for .ts files.
    // This can help map them correctly.
    '^(\\.{1,2}/.*)\\.js$': '$1',
  },
  coverageDirectory: '<rootDir>/coverage',
  collectCoverageFrom: [
    'src/**/*.{ts,js}',
    '!src/**/*.spec.{ts,js}',
    '!src/main.ts',
    '!src/main.server.ts',
    '!src/test-setup.ts',
    '!src/vite-env.d.ts',
    // Exclude generated files or config files not relevant for coverage
  ],
};
