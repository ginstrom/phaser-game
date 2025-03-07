import Phaser from 'phaser';

export interface InputFieldConfig {
    scene: Phaser.Scene;
    x: number;
    y: number;
    label: string;
    value?: string;
    labelStyle?: Phaser.Types.GameObjects.Text.TextStyle;
    inputStyle?: Phaser.Types.GameObjects.Text.TextStyle;
    backgroundColor?: number;
    backgroundAlpha?: number;
    padding?: {
        x: number;
        y: number;
    };
    width?: number;
    onTextChanged?: (text: string) => void;
}

export default class InputField extends Phaser.GameObjects.Container {
    private label: Phaser.GameObjects.Text;
    private inputBackground: Phaser.GameObjects.Rectangle;
    private inputText: Phaser.GameObjects.Text;
    private cursorGraphics: Phaser.GameObjects.Graphics;
    private isActive: boolean = false;
    private cursorVisible: boolean = false;
    private cursorTimer: Phaser.Time.TimerEvent | null = null;
    private onTextChanged: ((text: string) => void) | undefined;
    private fieldWidth: number;

    constructor(config: InputFieldConfig) {
        super(config.scene, config.x, config.y);

        // Default values
        const labelStyle = config.labelStyle || {
            color: '#ffffff',
            fontSize: '18px',
            fontFamily: 'Arial'
        };
        const inputStyle = config.inputStyle || {
            color: '#ffffff',
            fontSize: '18px',
            fontFamily: 'Arial'
        };
        const backgroundColor = config.backgroundColor !== undefined ? config.backgroundColor : 0x333333;
        const backgroundAlpha = config.backgroundAlpha !== undefined ? config.backgroundAlpha : 1;
        const padding = config.padding || { x: 10, y: 5 };
        this.fieldWidth = config.width || 200;
        this.onTextChanged = config.onTextChanged;

        // Create label
        this.label = new Phaser.GameObjects.Text(
            config.scene,
            -this.fieldWidth / 2,
            0,
            config.label,
            labelStyle
        );
        this.label.setOrigin(0, 0.5);

        // Create input background
        this.inputBackground = new Phaser.GameObjects.Rectangle(
            config.scene,
            0,
            this.label.height + 10,
            this.fieldWidth,
            30,
            backgroundColor,
            backgroundAlpha
        );
        this.inputBackground.setOrigin(0.5);
        this.inputBackground.setStrokeStyle(1, 0xffffff);

        // Create input text
        this.inputText = new Phaser.GameObjects.Text(
            config.scene,
            -this.fieldWidth / 2 + padding.x,
            this.label.height + 10,
            config.value || '',
            inputStyle
        );
        this.inputText.setOrigin(0, 0.5);

        // Create cursor graphics
        this.cursorGraphics = config.scene.add.graphics();
        this.updateCursorPosition();

        // Add to container
        this.add([this.label, this.inputBackground, this.inputText, this.cursorGraphics]);

        // Make interactive
        this.inputBackground.setInteractive({ useHandCursor: true })
            .on('pointerdown', this.onInputClick, this);

        // Add keyboard input
        this.scene.input.keyboard?.on('keydown', this.onKeyDown, this);

        // Add to scene
        config.scene.add.existing(this);

        // Handle clicking outside the input field
        this.scene.input.on('pointerdown', (pointer: Phaser.Input.Pointer) => {
            const bounds = this.inputBackground.getBounds();
            if (this.isActive && !bounds.contains(pointer.x, pointer.y)) {
                this.deactivate();
            }
        });
    }

    private onInputClick(): void {
        this.activate();
    }

    private activate(): void {
        if (!this.isActive) {
            this.isActive = true;
            this.inputBackground.setStrokeStyle(2, 0x00ff00);
            this.startCursorBlink();
        }
    }

    private deactivate(): void {
        if (this.isActive) {
            this.isActive = false;
            this.inputBackground.setStrokeStyle(1, 0xffffff);
            this.stopCursorBlink();
            this.cursorGraphics.clear();
        }
    }

    private onKeyDown(event: KeyboardEvent): void {
        if (!this.isActive) return;

        if (event.key === 'Backspace') {
            const text = this.inputText.text;
            if (text.length > 0) {
                this.setText(text.slice(0, -1));
            }
        } else if (event.key === 'Enter') {
            this.deactivate();
        } else if (event.key.length === 1) {
            // Only add printable characters
            this.setText(this.inputText.text + event.key);
        }
    }

    private startCursorBlink(): void {
        this.cursorVisible = true;
        this.updateCursorPosition();
        
        this.cursorTimer = this.scene.time.addEvent({
            delay: 500,
            callback: () => {
                this.cursorVisible = !this.cursorVisible;
                if (this.cursorVisible) {
                    this.updateCursorPosition();
                } else {
                    this.cursorGraphics.clear();
                }
            },
            loop: true
        });
    }

    private stopCursorBlink(): void {
        if (this.cursorTimer) {
            this.cursorTimer.destroy();
            this.cursorTimer = null;
        }
    }

    private updateCursorPosition(): void {
        const textWidth = this.inputText.width;
        const x = -this.fieldWidth / 2 + 10 + textWidth;
        const y = this.label.height + 10;
        
        this.cursorGraphics.clear();
        if (this.cursorVisible && this.isActive) {
            this.cursorGraphics.lineStyle(2, 0xffffff);
            this.cursorGraphics.lineBetween(x, y - 10, x, y + 10);
        }
    }

    public setText(text: string): this {
        this.inputText.setText(text);
        this.updateCursorPosition();
        
        if (this.onTextChanged) {
            this.onTextChanged(text);
        }
        
        return this;
    }

    public getText(): string {
        return this.inputText.text;
    }

    public destroy(fromScene?: boolean): void {
        this.stopCursorBlink();
        if (this.scene && this.scene.input && this.scene.input.keyboard) {
            this.scene.input.keyboard.off('keydown', this.onKeyDown, this);
        }
        super.destroy(fromScene);
    }
}
