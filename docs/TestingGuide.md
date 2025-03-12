# Testing Guide for Space Empire 4X Game

This document provides comprehensive information about testing in the Space Empire 4X game project.

## Test Stack

- Jest with React Testing Library for frontend
- Custom Phaser component testing utilities
- Webpack 5 test configuration
- Custom game state testing tools

## Running Tests

Use the project's test script to run tests:

```bash
./test.sh frontend
```

### Test Options

```bash
# Run tests in watch mode
npm run test:watch

# Generate coverage report
npm run test:coverage

# Run specific test file
npm test -- path/to/test/file.test.ts
```

## Test Structure

### Directory Structure

```
frontend/
├── src/
│   ├── __tests__/           # Test files
│   ├── __mocks__/          # Mock files
│   └── test-utils/         # Testing utilities
└── jest.config.js          # Jest configuration
```

### Test Categories

1. **Scene Tests**
   - Startup Scene
   - Main Scene
   - Galaxy Scene
   - System Scene
   - Planet Scene
   - Combat Scene

2. **Game System Tests**
   - Empire Management
   - Resource System
   - Fleet Management
   - Technology System
   - Map Generation

3. **UI Component Tests**
   - Custom Button System
   - Resource Display
   - Modal Windows
   - Context Menus
   - Tooltips

## Writing Tests

### Scene Testing

Example of testing a game scene:

```typescript
import { MainScene } from '../scenes/MainScene';

describe('MainScene', () => {
  let scene: MainScene;

  beforeEach(() => {
    scene = new MainScene();
  });

  it('should initialize with correct configuration', () => {
    expect(scene.sys.settings.key).toBe('MainScene');
  });

  it('should create menu buttons', () => {
    scene.create();
    expect(scene.buttons.length).toBeGreaterThan(0);
  });
});
```

### Game System Testing

Example of testing game systems:

```typescript
import { ResourceSystem } from '../systems/ResourceSystem';

describe('ResourceSystem', () => {
  let system: ResourceSystem;

  beforeEach(() => {
    system = new ResourceSystem();
  });

  it('should track resource production', () => {
    system.addResource('minerals', 100);
    expect(system.getResource('minerals')).toBe(100);
  });
});
```

### UI Component Testing

Example of testing UI components:

```typescript
import { Button } from '../ui/Button';

describe('Button', () => {
  it('should handle click events', () => {
    const onClick = jest.fn();
    const button = new Button({
      scene: mockScene,
      x: 100,
      y: 100,
      text: 'Test',
      onClick
    });

    button.emit('pointerdown');
    expect(onClick).toHaveBeenCalled();
  });
});
```

## Performance Testing

### Targets

- 60 FPS gameplay
- < 100ms response time
- < 2s initial load
- < 500KB initial bundle

### Tools

- Chrome DevTools Performance Panel
- Webpack Bundle Analyzer
- Custom FPS monitoring

## Best Practices

1. **Scene Testing**
   - Test scene initialization
   - Verify asset loading
   - Check scene transitions
   - Test game object creation

2. **Game Logic**
   - Unit test core mechanics
   - Test state management
   - Verify calculations
   - Test game rules

3. **UI Testing**
   - Test component rendering
   - Verify user interactions
   - Check responsive behavior
   - Test accessibility

4. **Performance Testing**
   - Monitor frame rate
   - Check memory usage
   - Verify load times
   - Test with varying conditions

## Troubleshooting

### Common Issues

1. **Scene Loading Failures**
   - Check asset paths
   - Verify scene configuration
   - Check for missing dependencies

2. **Game Object Issues**
   - Verify object creation
   - Check position calculations
   - Test collision detection

3. **Performance Problems**
   - Profile render calls
   - Check asset optimization
   - Monitor memory leaks

## Continuous Integration

Tests are run automatically on:
- Pull requests
- Main branch commits
- Release tags

Coverage reports are generated for:
- Scene tests
- System tests
- UI components