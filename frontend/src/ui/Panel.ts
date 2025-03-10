import Phaser from 'phaser';
import { TextStyles } from './TextStyles';

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
        this.add(this.background);

        // Create border if needed
        if (borderWidth > 0) {
            this.border = new Phaser.GameObjects.Rectangle(
                config.scene,
                0,
                0,
                config.width,
                config.height,
                borderColor
            );
            this.border.setOrigin(0.5);
            this.border.setStrokeStyle(borderWidth, borderColor);
            this.add(this.border);
        }

        // Create title if provided
        if (config.title) {
            this.titleText = new Phaser.GameObjects.Text(
                config.scene,
                0,
                -config.height / 2 + 20,
                config.title,
                config.titleStyle || TextStyles.panelTitle
            );
            this.titleText.setOrigin(0.5);
            this.add(this.titleText);
        }

        // Create content container
        this.contentContainer = new Phaser.GameObjects.Container(config.scene, 0, 0);
        this.add(this.contentContainer);

        // Set size
        super.setSize(config.width, config.height);

        // Make draggable if needed
        if (draggable) {
            this.setInteractive({ useHandCursor: true })
                .on('pointerdown', this.onDragStart, this)
                .on('pointermove', this.onDrag, this)
                .on('pointerup', this.onDragEnd, this)
                .on('pointerout', this.onDragEnd, this);
        }

        // Add to scene
        config.scene.add.existing(this);
    }

    addContent(content: Phaser.GameObjects.GameObject | Phaser.GameObjects.GameObject[]): this {
        if (Array.isArray(content)) {
            content.forEach(item => this.contentContainer.add(item));
        } else {
            this.contentContainer.add(content);
        }
        return this;
    }

    private onDragStart(pointer: Phaser.Input.Pointer): void {
        this.isDragging = true;
        this.dragStartX = pointer.x - this.x;
        this.dragStartY = pointer.y - this.y;
    }

    private onDrag(pointer: Phaser.Input.Pointer): void {
        if (this.isDragging) {
            this.setPosition(
                pointer.x - this.dragStartX,
                pointer.y - this.dragStartY
            );
        }
    }

    private onDragEnd(): void {
        this.isDragging = false;
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
