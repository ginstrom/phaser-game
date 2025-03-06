// Import jest-canvas-mock
require('jest-canvas-mock');

// Mock console.log to avoid cluttering test output
global.console = {
  ...console,
  log: jest.fn(),
  warn: jest.fn(),
  error: jest.fn(),
};
