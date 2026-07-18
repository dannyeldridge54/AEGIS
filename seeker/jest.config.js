module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/*.test.ts'],
  rootDir: __dirname,
  moduleFileExtensions: ['ts', 'js'],
};
