import Phaser from 'phaser';

export enum ButtonStyle {
    PRIMARY = 'primary',
    SECONDARY = 'secondary',
    DANGER = 'danger'
}

export interface ButtonConfig {
    scene: Phaser.Scene;
    x: number;
    y: number;
    text: string;
    style?: ButtonStyle;
    width?: number;
    height?: number;
    textStyle?: Phaser.Types.GameObjects.Text.TextStyle;
    callback?: () => void;
}

export class SciFiButton extends Phaser.GameObjects.Container {
    private background!: Phaser.GameObjects.Rectangle;
    private label!: Phaser.GameObjects.Text;
    private buttonStyle: ButtonStyle;
    private hoverTween: Phaser.Tweens.Tween | null = null;
    private clickTween: Phaser.Tweens.Tween | null = null;

    constructor(config: ButtonConfig) {
        super(config.scene, config.x, config.y);
        
        this.buttonStyle = config.style || ButtonStyle.PRIMARY;

        // Default values
        const width = config.width || 200;
        const height = config.height || 50;
        
        // Style mapping based on button type
        const styles = {
            [ButtonStyle.PRIMARY]: {
                bgColor: 0x4444FF,
                hoverColor: 0x8888FF,
                textColor: '#FFFFFF'
            },
            [ButtonStyle.SECONDARY]: {
                bgColor: 0x444444,
                hoverColor: 0x666666,
                textColor: '#FFFFFF'
            },
            [ButtonStyle.DANGER]: {
                bgColor: 0xFF4444,
                hoverColor: 0xFF8888,
                textColor: '#FFFFFF'
            }
        };
        
        const currentStyle = styles[this.buttonStyle];
        
        // Create background
        this.background = config.scene.add.rectangle(
            0, 0, width, height, currentStyle.bgColor
        );
        
        // Create text
        const defaultTextStyle = {
            fontFamily: 'monospace',
            fontSize: '24px',
            color: currentStyle.textColor,
            align: 'center'
        };
        
        this.label = config.scene.add.text(
            0, 0, 
            config.text,
            { ...defaultTextStyle, ...config.textStyle }
        );
        this.label.setOrigin(0.5);
        
        // Add components to container
        this.add([this.background, this.label]);
        
        // Make interactive
        this.setSize(width, height);
        this.setInteractive({ useHandCursor: true });
        
        // Setup events
        this.setupEvents(currentStyle.hoverColor, currentStyle.bgColor, config.callback);
        
        // Add to scene
        config.scene.add.existing(this);
    }
    
    private setupEvents(hoverColor: number, normalColor: number, callback?: () => void): void {
        // Hover effects
        this.on('pointerover', () => {
            this.background.setFillStyle(hoverColor);
            
            if (this.hoverTween) {
                this.hoverTween.stop();
            }
            
            this.hoverTween = this.scene.tweens.add({
                targets: this,
                scaleX: 1.05,
                scaleY: 1.05,
                duration: 100
            });
        });
        
        this.on('pointerout', () => {
            this.background.setFillStyle(normalColor);
            
            if (this.hoverTween) {
                this.hoverTween.stop();
            }
            
            this.hoverTween = this.scene.tweens.add({
                targets: this,
                scaleX: 1,
                scaleY: 1,
                duration: 100
            });
        });
        
        // Click effect
        this.on('pointerdown', () => {
            if (this.clickTween) {
                this.clickTween.stop();
            }
            
            this.clickTween = this.scene.tweens.add({
                targets: this,
                scaleX: 0.95,
                scaleY: 0.95,
                duration: 50,
                yoyo: true,
                onComplete: () => {
                    if (callback) {
                        callback();
                    }
                }
            });
        });
    }
    
    public setText(text: string): this {
        this.label.setText(text);
        return this;
    }
    
    public getText(): string {
        return this.label.text;
    }
    
    public setEnabled(enabled: boolean): this {
        if (enabled) {
            this.setAlpha(1);
            this.setInteractive();
        } else {
            this.setAlpha(0.6);
            this.disableInteractive();
        }
        return this;
    }

    public destroy(fromScene?: boolean): void {
        // Stop any active tweens
        if (this.hoverTween) {
            this.hoverTween.stop();
            this.hoverTween = null;
        }
        if (this.clickTween) {
            this.clickTween.stop();
            this.clickTween = null;
        }

        // Call parent destroy
        super.destroy(fromScene);
    }
}