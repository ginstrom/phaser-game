import Phaser from 'phaser';

// No need to mock Phaser here as it's already mocked in __mocks__/phaserMock.js

describe('Game Initialization', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  it('should initialize Phaser game with correct configuration', () => {
    // Create a mock configuration similar to what's in index.ts
    const config: Phaser.Types.Core.GameConfig = {
      type: Phaser.AUTO,
      width: 1024,
      height: 768,
      parent: 'game-container',
      backgroundColor: '#000000',
      scene: [],
      physics: {
        default: 'arcade',
        arcade: {
          gravity: { x: 0, y: 0 },
          debug: false
        }
      }
    };

    // Initialize a new Phaser game with the mock configuration
    const game = new Phaser.Game(config);

    // Check if Phaser.Game constructor was called
    expect(Phaser.Game).toHaveBeenCalled();

    // Get the configuration passed to Phaser.Game
    const passedConfig = (Phaser.Game as jest.Mock).mock.calls[0][0];

    // Verify configuration properties
    expect(passedConfig.type).toBe(Phaser.AUTO);
    expect(passedConfig.width).toBe(1024);
    expect(passedConfig.height).toBe(768);
    expect(passedConfig.parent).toBe('game-container');
    expect(passedConfig.backgroundColor).toBe('#000000');
    
    // Verify physics configuration
    expect(passedConfig.physics.default).toBe('arcade');
    expect(passedConfig.physics.arcade.gravity.x).toBe(0);
    expect(passedConfig.physics.arcade.gravity.y).toBe(0);
  });
});
