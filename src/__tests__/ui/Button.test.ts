import Button, { ButtonConfig } from '../../ui/Button';

describe('Button', () => {
  // Mock scene
  const mockScene = {
    add: {
      existing: jest.fn(),
    },
  };

  // Default button config
  const defaultConfig: ButtonConfig = {
    scene: mockScene as any,
    x: 100,
    y: 200,
    text: 'Test Button',
  };

  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  it('should create a button with default values', () => {
    // Create a button with default config
    const button = new Button(defaultConfig);

    // Check if the button was added to the scene
    expect(mockScene.add.existing).toHaveBeenCalledWith(button);
  });

  it('should create a button with custom values', () => {
    // Create a button with custom config
    const customConfig: ButtonConfig = {
      ...defaultConfig,
      textStyle: {
        color: '#ff0000',
        fontSize: '32px',
        fontFamily: 'Arial',
      },
      backgroundColor: 0xff0000,
      backgroundAlpha: 0.5,
      padding: {
        x: 30,
        y: 15,
      },
    };
    const button = new Button(customConfig);

    // Check if the button was added to the scene
    expect(mockScene.add.existing).toHaveBeenCalledWith(button);
  });

  it('should call the callback when clicked', () => {
    // Create a mock callback
    const mockCallback = jest.fn();

    // Create a button with the mock callback
    const button = new Button({
      ...defaultConfig,
      callback: mockCallback,
    });

    // Simulate a click by calling the onPointerUp method
    (button as any).onPointerUp();

    // Check if the callback was called
    expect(mockCallback).toHaveBeenCalled();
  });

  it('should update the text when setText is called', () => {
    // Create a button
    const button = new Button(defaultConfig);

    // Mock the setText method of the text object
    const mockSetText = jest.fn().mockReturnThis();
    (button as any).text = {
      setText: mockSetText,
      width: 100,
      height: 20,
    };

    // Mock the setSize method of the background object
    const mockSetSize = jest.fn().mockReturnThis();
    (button as any).background = {
      setSize: mockSetSize,
    };

    // Call the setText method
    const newText = 'New Button Text';
    button.setText(newText);

    // Check if the text was updated
    expect(mockSetText).toHaveBeenCalledWith(newText);

    // Check if the background size was updated
    expect(mockSetSize).toHaveBeenCalled();
  });

  it('should update the callback when setCallback is called', () => {
    // Create a button
    const button = new Button(defaultConfig);

    // Create a mock callback
    const mockCallback = jest.fn();

    // Call the setCallback method
    button.setCallback(mockCallback);

    // Simulate a click by calling the onPointerUp method
    (button as any).onPointerUp();

    // Check if the callback was called
    expect(mockCallback).toHaveBeenCalled();
  });

  it('should change alpha on pointer events', () => {
    // Create a button
    const button = new Button(defaultConfig);

    // Mock the setAlpha method of the background object
    const mockSetAlpha = jest.fn().mockReturnThis();
    (button as any).background = {
      setAlpha: mockSetAlpha,
    };

    // Simulate pointer events
    (button as any).onPointerOver();
    expect(mockSetAlpha).toHaveBeenCalledWith(0.8);

    (button as any).onPointerOut();
    expect(mockSetAlpha).toHaveBeenCalledWith(1);

    (button as any).onPointerDown();
    expect(mockSetAlpha).toHaveBeenCalledWith(0.5);

    (button as any).onPointerUp();
    expect(mockSetAlpha).toHaveBeenCalledWith(0.8);
  });
});
