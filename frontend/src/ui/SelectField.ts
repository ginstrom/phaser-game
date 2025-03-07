import Phaser from 'phaser';
import Button from './Button';

export interface SelectOption {
    value: string;
    label: string;
}

export interface SelectFieldConfig {
    scene: Phaser.Scene;
    x: number;
    y: number;
    label: string;
    options: SelectOption[];
    initialValue?: string;
    labelStyle?: Phaser.Types.GameObjects.Text.TextStyle;
    valueStyle?: Phaser.Types.GameObjects.Text.TextStyle;
    backgroundColor?: number;
    backgroundAlpha?: number;
    width?: number;
    onValueChanged?: (value: string) => void;
}

export default class SelectField extends Phaser.GameObjects.Container {
    private label: Phaser.GameObjects.Text;
    private valueBackground: Phaser.GameObjects.Rectangle;
    private valueText: Phaser.GameObjects.Text;
    private options: SelectOption[];
    private currentValue: string;
    private optionsContainer: Phaser.GameObjects.Container | null = null;
    private isOpen: boolean = false;
    private onValueChanged: ((value: string) => void) | undefined;
    private fieldWidth: number;

    constructor(config: SelectFieldConfig) {
        super(config.scene, config.x, config.y);

        // Default values
        const labelStyle = config.labelStyle || {
            color: '#ffffff',
            fontSize: '18px',
            fontFamily: 'Arial'
        };
        const valueStyle = config.valueStyle || {
            color: '#ffffff',
            fontSize: '18px',
            fontFamily: 'Arial'
        };
        const backgroundColor = config.backgroundColor !== undefined ? config.backgroundColor : 0x333333;
        const backgroundAlpha = config.backgroundAlpha !== undefined ? config.backgroundAlpha : 1;
        this.fieldWidth = config.width || 200;
        this.options = config.options;
        this.onValueChanged = config.onValueChanged;

        // Set initial value
        const initialOption = this.options.find(opt => opt.value === config.initialValue);
        this.currentValue = initialOption ? initialOption.value : this.options[0].value;

        // Create label
        this.label = new Phaser.GameObjects.Text(
            config.scene,
            -this.fieldWidth / 2,
            0,
            config.label,
            labelStyle
        );
        this.label.setOrigin(0, 0.5);

        // Create value background
        this.valueBackground = new Phaser.GameObjects.Rectangle(
            config.scene,
            0,
            this.label.height + 10,
            this.fieldWidth,
            30,
            backgroundColor,
            backgroundAlpha
        );
        this.valueBackground.setOrigin(0.5);
        this.valueBackground.setStrokeStyle(1, 0xffffff);

        // Create value text
        const currentOptionLabel = this.getOptionLabel(this.currentValue);
        this.valueText = new Phaser.GameObjects.Text(
            config.scene,
            0,
            this.label.height + 10,
            currentOptionLabel,
            valueStyle
        );
        this.valueText.setOrigin(0.5);

        // Add dropdown arrow
        const arrowText = this.scene.add.text(
            this.fieldWidth / 2 - 20,
            this.label.height + 10,
            '▼',
            valueStyle
        );
        arrowText.setOrigin(0.5);

        // Add to container
        this.add([this.label, this.valueBackground, this.valueText, arrowText]);

        // Make interactive
        this.valueBackground.setInteractive({ useHandCursor: true })
            .on('pointerdown', this.toggleOptions, this);

        // Add to scene
        config.scene.add.existing(this);

        // Handle clicking outside the select field
        this.scene.input.on('pointerdown', (pointer: Phaser.Input.Pointer) => {
            if (this.isOpen) {
                const bounds = this.valueBackground.getBounds();
                if (!bounds.contains(pointer.x, pointer.y)) {
                    // Check if the click is within the options container
                    if (this.optionsContainer) {
                        const optionsBounds = this.optionsContainer.getBounds();
                        if (!optionsBounds.contains(pointer.x, pointer.y)) {
                            this.closeOptions();
                        }
                    } else {
                        this.closeOptions();
                    }
                }
            }
        });

        // Clean up event listener when destroyed
        this.on('destroy', () => {
            this.scene.input.off('pointerdown');
        });
    }

    private getOptionLabel(value: string): string {
        const option = this.options.find(opt => opt.value === value);
        return option ? option.label : '';
    }

    private toggleOptions(): void {
        if (this.isOpen) {
            this.closeOptions();
        } else {
            this.openOptions();
        }
    }

    private openOptions(): void {
        if (this.isOpen) return;

        this.isOpen = true;
        this.valueBackground.setStrokeStyle(2, 0x00ff00);

        // Create options container
        this.optionsContainer = new Phaser.GameObjects.Container(
            this.scene,
            0,
            this.label.height + 10 + 15 + this.options.length * 15
        );

        // Create options background
        const optionsBackground = new Phaser.GameObjects.Rectangle(
            this.scene,
            0,
            0,
            this.fieldWidth,
            this.options.length * 30,
            0x333333,
            1
        );
        optionsBackground.setOrigin(0.5, 1);
        optionsBackground.setStrokeStyle(1, 0xffffff);

        this.optionsContainer.add(optionsBackground);

        // Create option buttons
        this.options.forEach((option, index) => {
            const y = -this.options.length * 30 + index * 30 + 15;
            
            const optionText = new Phaser.GameObjects.Text(
                this.scene,
                0,
                y,
                option.label,
                { color: '#ffffff', fontSize: '18px', fontFamily: 'Arial' }
            );
            optionText.setOrigin(0.5);
            
            // Highlight the current value
            if (option.value === this.currentValue) {
                optionText.setColor('#ffff00');
            }
            
            // Make option interactive
            const optionBackground = new Phaser.GameObjects.Rectangle(
                this.scene,
                0,
                y,
                this.fieldWidth,
                30,
                0x333333,
                0
            );
            optionBackground.setOrigin(0.5);
            optionBackground.setInteractive({ useHandCursor: true })
                .on('pointerover', () => {
                    optionBackground.setFillStyle(0x444444);
                })
                .on('pointerout', () => {
                    optionBackground.setFillStyle(0x333333, 0);
                })
                .on('pointerdown', () => {
                    this.setValue(option.value);
                    this.closeOptions();
                });
            
            // We know optionsContainer is not null here because we just created it
            this.optionsContainer!.add([optionBackground, optionText]);
        });

        this.add(this.optionsContainer);
    }

    private closeOptions(): void {
        if (!this.isOpen) return;

        this.isOpen = false;
        this.valueBackground.setStrokeStyle(1, 0xffffff);

        if (this.optionsContainer) {
            this.optionsContainer.destroy();
            this.optionsContainer = null;
        }
    }

    public setValue(value: string): this {
        if (this.options.some(opt => opt.value === value)) {
            this.currentValue = value;
            this.valueText.setText(this.getOptionLabel(value));
            
            if (this.onValueChanged) {
                this.onValueChanged(value);
            }
        }
        
        return this;
    }

    public getValue(): string {
        return this.currentValue;
    }

    public destroy(fromScene?: boolean): void {
        this.closeOptions();
        super.destroy(fromScene);
    }
}
