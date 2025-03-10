// Mock all scene imports first
jest.mock('../scenes/StartupScene', () => ({}));
jest.mock('../scenes/GalaxyScene', () => ({}));
jest.mock('../scenes/SystemScene', () => ({}));
jest.mock('../scenes/PlanetScene', () => ({}));
jest.mock('../scenes/MainScene', () => ({}));

// Import the mock Phaser module
import mockPhaser from '../__mocks__/phaser';

describe('Game Initialization', () => {
    beforeEach(() => {
        (mockPhaser.Game as jest.Mock).mockClear();
        jest.resetModules();
    });

    it('should initialize game with correct configuration', () => {
        // Import the index file to trigger game initialization
        jest.isolateModules(() => {
            require('../index');
        });

        // Verify that the Game constructor was called
        expect(mockPhaser.Game).toHaveBeenCalledTimes(1);
        
        // Get and verify the configuration
        const config = (mockPhaser.Game as jest.Mock).mock.calls[0][0];
        expect(config).toEqual(expect.objectContaining({
            type: 'auto',
            width: 1024,
            height: 768,
            parent: 'game-container',
            backgroundColor: '#000000',
            physics: expect.objectContaining({
                default: 'arcade',
                arcade: expect.objectContaining({
                    gravity: { x: 0, y: 0 },
                    debug: false
                })
            })
        }));
        
        // Check that scenes array exists and has correct length
        expect(config.scene).toHaveLength(5);
    });
}); 