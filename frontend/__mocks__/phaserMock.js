// Mock Phaser
const MockGame = jest.fn().mockImplementation(() => ({
  // Mock game instance methods if needed
}));
class MockScene {
  constructor(config) {
    this.scene = {
      key: config,
      start: jest.fn(),
    };
  }
  add = {
    existing: jest.fn(),
    text: jest.fn().mockReturnValue({
      setOrigin: jest.fn().mockReturnThis(),
    }),
    graphics: jest.fn().mockReturnValue({
      clear: jest.fn().mockReturnThis(),
      lineStyle: jest.fn().mockReturnThis(),
      lineBetween: jest.fn().mockReturnThis(),
    }),
  };
  cameras = {
    main: {
      width: 1024,
      height: 768,
    },
  };
  input = {
    keyboard: {
      on: jest.fn(),
      off: jest.fn(),
    },
    on: jest.fn(),
  };
  time = {
    addEvent: jest.fn().mockReturnValue({
      destroy: jest.fn(),
    }),
  };
}

// Mock Phaser namespace
const Phaser = {
  Game: MockGame,
  Scene: MockScene,
  AUTO: 'auto',
  GameObjects: {
    Container: class {
      constructor(scene, x, y) {
        this.scene = scene;
        this.x = x;
        this.y = y;
        this.list = [];
      }
      add = jest.fn().mockReturnThis();
      setSize = jest.fn().mockReturnThis();
      setInteractive = jest.fn().mockReturnThis();
      on = jest.fn().mockReturnThis();
    },
    Rectangle: class {
      constructor(scene, x, y, width, height, color, alpha) {
        this.scene = scene;
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
        this.color = color;
        this.alpha = alpha;
      }
      setAlpha = jest.fn().mockReturnThis();
      setSize = jest.fn().mockReturnThis();
      setOrigin = jest.fn().mockReturnThis();
      setStrokeStyle = jest.fn().mockReturnThis();
      setInteractive = jest.fn().mockReturnThis();
      on = jest.fn().mockReturnThis();
      getBounds = jest.fn().mockReturnValue({
        contains: jest.fn().mockReturnValue(false)
      });
    },
    Text: class {
      constructor(scene, x, y, text, style) {
        this.scene = scene;
        this.x = x;
        this.y = y;
        this.text = text;
        this.style = style;
        this.width = 100;
        this.height = 20;
      }
      setOrigin = jest.fn().mockReturnThis();
      setText = jest.fn().mockReturnThis();
    },
    GameObject: class {
      constructor(scene) {
        this.scene = scene;
      }
    },
    Graphics: class {
      constructor(scene) {
        this.scene = scene;
      }
      clear = jest.fn().mockReturnThis();
      lineStyle = jest.fn().mockReturnThis();
      lineBetween = jest.fn().mockReturnThis();
    },
  },
  Types: {
    Core: {
      GameConfig: {},
    },
    GameObjects: {
      Text: {
        TextStyle: {},
      },
    },
  },
  Input: {
    Pointer: class {
      constructor() {
        this.x = 0;
        this.y = 0;
      }
    },
  },
  Physics: {
    Arcade: {
      ArcadePhysics: class {
        constructor() {
          this.gravity = { x: 0, y: 0 };
        }
      }
    }
  }
};

// Add GameObject to the prototype chain
Phaser.GameObjects.Container.prototype = Object.create(Phaser.GameObjects.GameObject.prototype);
Phaser.GameObjects.Rectangle.prototype = Object.create(Phaser.GameObjects.GameObject.prototype);
Phaser.GameObjects.Text.prototype = Object.create(Phaser.GameObjects.GameObject.prototype);
Phaser.GameObjects.Graphics.prototype = Object.create(Phaser.GameObjects.GameObject.prototype);

module.exports = Phaser;
