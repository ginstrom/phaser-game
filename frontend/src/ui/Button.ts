import Phaser from 'phaser';

export interface ButtonConfig {
    scene: Phaser.Scene;
    x: number;
    y: number;
    text: string;
    textStyle?: Phaser.Types.GameObjects.Text.TextStyle;
    backgroundColor?: number;
    backgroundAlpha?: number;
    padding?: {
        x: number;
        y: number;
    };
    callback?: () => void;
}

export default class Button extends Phaser.GameObjects.Container {
    private background: Phaser.GameObjects.Rectangle;
    private text: Phaser.GameObjects.Text;
    private callback: (() => void) | undefined;
    private enabled: boolean = true;

    constructor(config: ButtonConfig) {
        super(config.scene, config.x, config.y);

        // Default values
        const textStyle = config.textStyle || {
            color: '#ffffff',
            fontSize: '24px',
            fontFamily: 'Arial'
        };
        const backgroundColor = config.backgroundColor !== undefined ? config.backgroundColor : 0x4a6fa5;
        const backgroundAlpha = config.backgroundAlpha !== undefined ? config.backgroundAlpha : 1;
        const padding = config.padding || { x: 20, y: 10 };

        // Create text
        this.text = new Phaser.GameObjects.Text(
            config.scene,
            0,
            0,
            config.text,
            textStyle
        );
        this.text.setOrigin(0.5);

        // Create background
        const width = this.text.width + padding.x * 2;
        const height = this.text.height + padding.y * 2;
        this.background = new Phaser.GameObjects.Rectangle(
            config.scene,
            0,
            0,
            width,
            height,
            backgroundColor,
            backgroundAlpha
        );

        // Add to container
        this.add([this.background, this.text]);

        // Set callback
        this.callback = config.callback;

        // Make interactive
        this.setSize(width, height);
        this.setInteractive({ useHandCursor: true })
            .on('pointerover', this.onPointerOver, this)
            .on('pointerout', this.onPointerOut, this)
            .on('pointerdown', this.onPointerDown, this)
            .on('pointerup', this.onPointerUp, this);

        // Add to scene
        config.scene.add.existing(this);
    }

    private onPointerOver(): void {
        this.background.setAlpha(0.8);
    }

    private onPointerOut(): void {
        this.background.setAlpha(1);
    }

    private onPointerDown(): void {
        this.background.setAlpha(0.5);
    }

    private onPointerUp(): void {
        this.background.setAlpha(0.8);
        if (this.callback && this.enabled) {
            this.callback();
        }
    }

    public setCallback(callback: () => void): this {
        this.callback = callback;
        return this;
    }

    public setText(text: string): this {
        this.text.setText(text);
        
        // Resize background to fit new text
        const width = this.text.width + 40;
        const height = this.text.height + 20;
        this.background.setSize(width, height);
        this.setSize(width, height);
        
        return this;
    }

    /**
     * Enable or disable the button
     * @param enabled Whether the button should be enabled
     */
    public setEnabled(enabled: boolean): this {
        this.enabled = enabled;
        
        // Visual feedback for disabled state
        if (enabled) {
            this.background.setAlpha(1);
            this.text.setAlpha(1);
        } else {
            this.background.setAlpha(0.5);
            this.text.setAlpha(0.5);
        }
        
        return this;
    }

    /**
     * Check if the button is enabled
     */
    public isEnabled(): boolean {
        return this.enabled;
    }
}
