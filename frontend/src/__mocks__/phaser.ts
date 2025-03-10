// Mock Phaser classes and types
class Scene {
    add = {
        text: jest.fn().mockImplementation((x, y, text, style) => {
            const textObj = new Text(this, x, y, text, style);
            return textObj;
        }),
        circle: jest.fn().mockImplementation((x, y, radius) => {
            const circle = new GameObject(this, x, y);
            (circle as any).setStrokeStyle = jest.fn().mockReturnThis();
            return circle;
        }),
        rectangle: jest.fn().mockImplementation((x, y, width, height, color, alpha) => {
            const rect = new Rectangle(this, x, y, width, height, color, alpha);
            return rect;
        }),
        container: jest.fn().mockImplementation((x, y) => {
            return new Container(this, x, y);
        }),
        existing: jest.fn().mockReturnThis()
    };
    cameras = {
        main: {
            width: 800,
            height: 600
        }
    };
    scene = {
        start: jest.fn()
    };
}

// Base mock methods that all game objects share
const createBaseMethods = () => ({
    setPosition: jest.fn().mockReturnThis(),
    setSize: jest.fn().mockReturnThis(),
    setInteractive: jest.fn().mockReturnThis(),
    on: jest.fn().mockReturnThis(),
    destroy: jest.fn(),
    setOrigin: jest.fn().mockReturnThis(),
    setAlpha: jest.fn().mockReturnThis(),
});

// Container-specific methods
const createContainerMethods = () => ({
    add: jest.fn().mockReturnThis(),
    addAt: jest.fn().mockReturnThis(),
    remove: jest.fn().mockReturnThis(),
    removeAll: jest.fn().mockReturnThis(),
    disableInteractive: jest.fn().mockReturnThis(),
});

// Type declarations for mixin methods
interface BaseMethods {
    setPosition: (x: number, y: number) => any;
    setSize: (width: number, height: number) => any;
    setInteractive: (config?: any) => any;
    on: (event: string, fn: Function, context?: any) => any;
    destroy: () => void;
    setOrigin: (x: number, y?: number) => any;
    setAlpha: (alpha: number) => any;
}

interface ContainerMethods {
    add: (items: GameObject | GameObject[]) => any;
    addAt: (item: GameObject, index: number) => any;
    remove: (item: GameObject) => any;
    removeAll: (destroyChild?: boolean) => any;
    disableInteractive: () => any;
}

class GameObject implements BaseMethods {
    scene: Scene;
    x: number;
    y: number;
    width: number = 0;
    height: number = 0;
    alpha: number = 1;
    origin = { x: 0.5, y: 0.5 };

    constructor(scene: Scene, x: number, y: number) {
        this.scene = scene;
        this.x = x;
        this.y = y;
        this.initMethods();
    }

    protected initMethods() {
        this.setPosition = jest.fn().mockImplementation((x: number, y: number) => {
            this.x = x;
            this.y = y;
            return this;
        });
        this.setSize = jest.fn().mockImplementation((width: number, height: number) => {
            this.width = width;
            this.height = height;
            return this;
        });
        this.setInteractive = jest.fn().mockReturnThis();
        this.on = jest.fn().mockReturnThis();
        this.destroy = jest.fn();
        this.setOrigin = jest.fn().mockReturnThis();
        this.setAlpha = jest.fn().mockReturnThis();
    }

    setPosition!: (x: number, y: number) => this;
    setSize!: (width: number, height: number) => this;
    setInteractive!: (config?: any) => this;
    on!: (event: string, fn: Function, context?: any) => this;
    destroy!: () => void;
    setOrigin!: (x: number, y?: number) => this;
    setAlpha!: (alpha: number) => this;
}

class Container extends GameObject implements ContainerMethods {
    list: GameObject[] = [];

    constructor(scene: Scene, x: number, y: number) {
        super(scene, x, y);
        this.initContainerMethods();
    }

    protected initContainerMethods() {
        this.add = jest.fn().mockImplementation((items: GameObject | GameObject[]) => {
            if (Array.isArray(items)) {
                this.list.push(...items);
            } else {
                this.list.push(items);
            }
            return this;
        });
        this.addAt = jest.fn().mockReturnThis();
        this.remove = jest.fn().mockReturnThis();
        this.removeAll = jest.fn().mockReturnThis();
        this.disableInteractive = jest.fn().mockReturnThis();
    }

    add!: (items: GameObject | GameObject[]) => this;
    addAt!: (item: GameObject, index: number) => this;
    remove!: (item: GameObject) => this;
    removeAll!: (destroyChild?: boolean) => this;
    disableInteractive!: () => this;
}

// Ensure Container inherits from GameObject
Object.setPrototypeOf(Container.prototype, GameObject.prototype);

class Text extends GameObject {
    content: string;
    style: any;
    setText = jest.fn().mockReturnThis();
    setWordWrapWidth = jest.fn().mockReturnThis();

    constructor(scene: Scene, x: number, y: number, text: string, style?: any) {
        super(scene, x, y);
        this.content = text;
        this.style = style;
    }
}

class Rectangle extends GameObject {
    fillColor: number;
    fillAlpha: number;
    setStrokeStyle = jest.fn().mockReturnThis();
    setFillStyle = jest.fn().mockReturnThis();

    constructor(scene: Scene, x: number, y: number, width: number, height: number, color?: number, alpha?: number) {
        super(scene, x, y);
        this.fillColor = color || 0x000000;
        this.fillAlpha = alpha !== undefined ? alpha : 1;
        this.setSize(width, height);
    }
}

class GameObjects {
    static Container = Container;
    static Text = Text;
    static Rectangle = Rectangle;
    static GameObject = GameObject;
}

const AUTO = 'AUTO';

interface PhaserMath {
    Between: jest.Mock;
    PI2: number;
}

const PhaserMath: PhaserMath = {
    Between: jest.fn().mockReturnValue(0),
    PI2: Math.PI * 2
};

const Types = {
    Core: {
        GameConfig: {}
    },
    GameObjects: {
        GameObjectConfig: {},
        Container: Container,
        Text: Text,
        Rectangle: Rectangle
    }
};

const Input = {
    Keyboard: {
        KeyCodes: {
            SPACE: 32,
            ENTER: 13
        }
    }
};

// Create Game constructor as a proper Jest mock
const Game = jest.fn().mockImplementation(function(this: any, config: any) {
    this.config = config;
    this.destroy = jest.fn();
    return this;
});

// Add Jest mock properties
Game.mockClear();
Game.mockReset();

// Add mock property with arrays for tracking calls
Game.mock = {
    calls: [],
    instances: [],
    results: [],
    contexts: [],
    invocationCallOrder: []
};

const mockGame = jest.fn();

const mockPhaser = {
    Game: mockGame,
    AUTO: 'auto',
    Types: {
        Core: {
            GameConfig: {}
        }
    },
    Physics: {
        Arcade: {
            Sprite: jest.fn()
        }
    }
};

export default mockPhaser; 