import StartupScene from '../../scenes/StartupScene';
import Button from '../../ui/Button';

// Mock the Button class
jest.mock('../../ui/Button', () => {
  return jest.fn().mockImplementation(() => ({
    setCallback: jest.fn().mockReturnThis(),
  }));
});

describe('StartupScene', () => {
  let scene: StartupScene;

  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
    
    // Create a new instance of StartupScene
    scene = new StartupScene();
  });

  it('should be initialized with the correct key', () => {
    expect(scene.scene.key).toBe('StartupScene');
  });

  describe('create method', () => {
    beforeEach(() => {
      // Call the create method
      scene.create();
    });

    it('should add title text', () => {
      expect(scene.add.text).toHaveBeenCalledWith(
        expect.any(Number),
        expect.any(Number),
        '4X Space Empire',
        expect.any(Object)
      );
    });

    it('should add subtitle text', () => {
      expect(scene.add.text).toHaveBeenCalledWith(
        expect.any(Number),
        expect.any(Number),
        'A Turn-Based Strategy Game',
        expect.any(Object)
      );
    });

    it('should create buttons', () => {
      // Check if Button constructor was called 4 times (New Game, Load Game, Settings, Exit)
      expect(Button).toHaveBeenCalledTimes(4);
      
      // Check if the first button is the New Game button
      expect(Button).toHaveBeenCalledWith(
        expect.objectContaining({
          scene: scene,
          text: 'New Game',
        })
      );
    });
  });

  describe('button callbacks', () => {
    beforeEach(() => {
      // Spy on console.log
      jest.spyOn(console, 'log');
      
      // Spy on scene.start
      jest.spyOn(scene.scene, 'start');
      
      // Call the create method to set up buttons
      scene.create();
    });

    it('should open new game dialog when New Game button is clicked', () => {
      // Get the callback from the first Button constructor call
      const mockButton = jest.mocked(Button);
      const newGameCallback = mockButton.mock.calls[0][0].callback;
      
      // Call the callback
      if (newGameCallback) {
        newGameCallback();
      }
      
      // Check if console.log was called with the expected message
      expect(console.log).toHaveBeenCalledWith('Starting new game');
    });

    it('should log message when Load Game button is clicked', () => {
      // Get the callback from the second Button constructor call
      const mockButton = jest.mocked(Button);
      const loadGameCallback = mockButton.mock.calls[1][0].callback;
      
      // Call the callback
      if (loadGameCallback) {
        loadGameCallback();
      }
      
      // Check if console.log was called with the expected message
      expect(console.log).toHaveBeenCalledWith(expect.stringContaining('Load game'));
    });

    it('should log message when Settings button is clicked', () => {
      // Get the callback from the third Button constructor call
      const mockButton = jest.mocked(Button);
      const settingsCallback = mockButton.mock.calls[2][0].callback;
      
      // Call the callback
      if (settingsCallback) {
        settingsCallback();
      }
      
      // Check if console.log was called with the expected message
      expect(console.log).toHaveBeenCalledWith(expect.stringContaining('Settings'));
    });

    it('should log message when Exit button is clicked', () => {
      // Get the callback from the fourth Button constructor call
      const mockButton = jest.mocked(Button);
      const exitCallback = mockButton.mock.calls[3][0].callback;
      
      // Call the callback
      if (exitCallback) {
        exitCallback();
      }
      
      // Check if console.log was called with the expected message
      expect(console.log).toHaveBeenCalledWith(expect.stringContaining('Exit'));
    });
  });
});
