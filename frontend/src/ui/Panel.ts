import Phaser from 'phaser';

export interface PanelConfig {
    scene: Phaser.Scene;
    x: number;
    y: number;
    width: number;
    height: number;
    backgroundColor?: number;
    backgroundAlpha?: number;
    borderColor?: number;
    borderWidth?: number;
    cornerRadius?: number;
    title?: string;
    titleStyle?: Phaser.Types.GameObjects.Text.TextStyle;
    draggable?: boolean;
}

export default class Panel extends Phaser.GameObjects.Container {
    private background: Phaser.GameObjects.Rectangle;
    private border: Phaser.GameObjects.Rectangle | null = null;
    private titleText: Phaser.GameObjects.Text | null = null;
    private contentContainer: Phaser.GameObjects.Container;
    private isDragging: boolean = false;
    private dragStartX: number = 0;
    private dragStartY: number = 0;

    constructor(config: PanelConfig) {
        super(config.scene, config.x, config.y);

        // Default values
        const backgroundColor = config.backgroundColor !== undefined ? config.backgroundColor : 0x000000;
        const backgroundAlpha = config.backgroundAlpha !== undefined ? config.backgroundAlpha : 0.8;
        const borderColor = config.borderColor !== undefined ? config.borderColor : 0x4a6fa5;
        const borderWidth = config.borderWidth !== undefined ? config.borderWidth : 2;
        const cornerRadius = config.cornerRadius !== undefined ? config.cornerRadius : 0;
        const draggable = config.draggable !== undefined ? config.draggable : false;

        // Create background
        this.background = new Phaser.GameObjects.Rectangle(
            config.scene,
            0,
            0,
            config.width,
            config.height,
            backgroundColor,
            backgroundAlpha
        );
        this.background.setOrigin(0.5);

        // Create border if needed
        if (borderWidth > 0) {
            this.border = new Phaser.GameObjects.Rectangle(
                config.scene,
                0,
                0,
                config.width,
                config.height,
                borderColor,
                1
            );
            this.border.setOrigin(0.5);
            this.border.setStrokeStyle(borderWidth, borderColor);
        }

        // Create title if needed
        if (config.title) {
            const titleStyle = config.titleStyle || {
                color: '#ffffff',
                fontSize: '24px',
                fontFamily: 'Arial',
                fontStyle: 'bold'
            };
            
            this.titleText = new Phaser.GameObjects.Text(
                config.scene,
                0,
                -config.height / 2 + 20,
                config.title,
                titleStyle
            );
            this.titleText.setOrigin(0.5);
        }

        // Create content container
        this.contentContainer = new Phaser.GameObjects.Container(
            config.scene,
            0,
            this.titleText ? 10 : 0
        );

        // Add to container
        this.add(this.background);
        if (this.border) this.add(this.border);
        if (this.titleText) this.add(this.titleText);
        this.add(this.contentContainer);

        // Set size
        this.setSize(config.width, config.height);

        // Make draggable if needed
        if (draggable) {
            this.setInteractive({ useHandCursor: true, draggable: true })
                .on('dragstart', this.onDragStart, this)
                .on('drag', this.onDrag, this)
                .on('dragend', this.onDragEnd, this);
        }

        // Add to scene
        config.scene.add.existing(this);
    }

    private onDragStart(pointer: Phaser.Input.Pointer): void {
        this.isDragging = true;
        this.dragStartX = pointer.x - this.x;
        this.dragStartY = pointer.y - this.y;
    }

    private onDrag(pointer: Phaser.Input.Pointer): void {
        if (this.isDragging) {
            this.x = pointer.x - this.dragStartX;
            this.y = pointer.y - this.dragStartY;
        }
    }

    private onDragEnd(): void {
        this.isDragging = false;
    }

    public addContent(gameObject: Phaser.GameObjects.GameObject | Phaser.GameObjects.GameObject[]): this {
        this.contentContainer.add(gameObject);
        return this;
    }

    public clearContent(): this {
        this.contentContainer.removeAll(true);
        return this;
    }

    public setTitle(title: string): this {
        if (this.titleText) {
            this.titleText.setText(title);
        }
        return this;
    }
}
