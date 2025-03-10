import Phaser from 'phaser';
import { TextStyles } from './TextStyles';

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
        const backgroundColor = config.backgroundColor !== undefined ? config.backgroundColor : 0x4a6fa5;
        const backgroundAlpha = config.backgroundAlpha !== undefined ? config.backgroundAlpha : 1;
        const padding = config.padding || { x: 20, y: 10 };
        this.callback = config.callback;

        // Create text
        this.text = new Phaser.GameObjects.Text(
            config.scene,
            0,
            0,
            config.text,
            config.textStyle || TextStyles.button
        );
        this.text.setOrigin(0.5);

        // Calculate size
        const width = this.text.width + padding.x * 2;
        const height = this.text.height + padding.y * 2;

        // Create background
        this.background = new Phaser.GameObjects.Rectangle(
            config.scene,
            0,
            0,
            width,
            height,
            backgroundColor,
            backgroundAlpha
        );
        this.background.setOrigin(0.5);

        // Add to container
        this.add([this.background, this.text]);

        // Set size
        super.setSize(width, height);

        // Make interactive
        this.setInteractive({ useHandCursor: true })
            .on('pointerover', this.onPointerOver, this)
            .on('pointerout', this.onPointerOut, this)
            .on('pointerdown', this.onPointerDown, this)
            .on('pointerup', this.onPointerUp, this);

        // Add to scene
        config.scene.add.existing(this);
    }

    private onPointerOver(): void {
        if (this.enabled) {
            this.text.setAlpha(0.8);
        }
    }

    private onPointerOut(): void {
        if (this.enabled) {
            this.text.setAlpha(1);
        }
    }

    private onPointerDown(): void {
        if (this.enabled) {
            this.text.setAlpha(0.5);
        }
    }

    private onPointerUp(): void {
        if (this.enabled) {
            this.text.setAlpha(1);
            if (this.callback) {
                this.callback();
            }
        }
    }

    public setCallback(callback: () => void): this {
        this.callback = callback;
        return this;
    }

    public setText(text: string): this {
        this.text.setText(text);

        // Recalculate size
        const padding = { x: 20, y: 10 }; // Use default padding
        const width = this.text.width + padding.x * 2;
        const height = this.text.height + padding.y * 2;

        // Update background size
        this.background.setSize(width, height);

        // Update container size
        super.setSize(width, height);

        return this;
    }

    public setEnabled(enabled: boolean): this {
        this.enabled = enabled;
        if (enabled) {
            this.text.setAlpha(1);
            this.background.setAlpha(1);
            this.setInteractive();
        } else {
            this.text.setAlpha(0.5);
            this.background.setAlpha(0.5);
            this.disableInteractive();
        }
        return this;
    }

    public isEnabled(): boolean {
        return this.enabled;
    }
}
