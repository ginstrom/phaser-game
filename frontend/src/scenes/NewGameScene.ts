import Phaser from 'phaser';

export class NewGameScene extends Phaser.Scene {
    private formInputs!: {
        empireName: Phaser.GameObjects.Text;
        computerCount: Phaser.GameObjects.Text;
        galaxySize: Phaser.GameObjects.Text;
        selectedSize: string;
    };
    private currentInput: 'empireName' | 'computerCount' | null = null;
    private keyboard!: Phaser.Input.Keyboard.KeyboardPlugin;
    private errorMessage: Phaser.GameObjects.Text | null = null;

    constructor() {
        super({ key: 'NewGameScene' });
        this.formInputs = {
            empireName: null!,
            computerCount: null!,
            galaxySize: null!,
            selectedSize: 'small'
        };
        this.errorMessage = null;
    }

    private showError(message: string) {
        if (this.errorMessage) {
            this.errorMessage.destroy();
        }

        this.errorMessage = this.add.text(
            this.cameras.main.centerX,
            this.cameras.main.height - 50,
            message,
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#ff0000',
                align: 'center',
                backgroundColor: '#330000',
                padding: { x: 10, y: 5 }
            }
        ).setOrigin(0.5);

        // Auto-hide after 5 seconds
        this.time.delayedCall(5000, () => {
            if (this.errorMessage) {
                this.errorMessage.destroy();
                this.errorMessage = null;
            }
        });
    }

    create() {
        // Set black background
        this.cameras.main.setBackgroundColor('#000000');

        // Title
        const title = this.add.text(
            this.cameras.main.centerX,
            50,
            'New Game Setup',
            {
                fontFamily: 'monospace',
                fontSize: '36px',
                color: '#00ff00',
                align: 'center'
            }
        ).setOrigin(0.5);

        // Empire Name Input
        this.add.text(
            this.cameras.main.centerX - 200,
            150,
            'Empire Name:',
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#ffffff'
            }
        );

        this.formInputs.empireName = this.add.text(
            this.cameras.main.centerX + 50,
            150,
            'My Empire',
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#ffff00',
                backgroundColor: '#333333',
                padding: { x: 10, y: 5 }
            }
        ).setInteractive();

        // Computer Empire Count
        this.add.text(
            this.cameras.main.centerX - 200,
            250,
            'Computer Empires:',
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#ffffff'
            }
        );

        this.formInputs.computerCount = this.add.text(
            this.cameras.main.centerX + 50,
            250,
            '3',
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#ffff00',
                backgroundColor: '#333333',
                padding: { x: 10, y: 5 }
            }
        ).setInteractive();

        // Galaxy Size
        this.add.text(
            this.cameras.main.centerX - 200,
            350,
            'Galaxy Size:',
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#ffffff'
            }
        );

        const sizes = ['tiny', 'small', 'medium', 'large'];
        this.formInputs.galaxySize = this.add.text(
            this.cameras.main.centerX + 50,
            350,
            this.formInputs.selectedSize,
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#ffff00',
                backgroundColor: '#333333',
                padding: { x: 10, y: 5 }
            }
        ).setInteractive();

        this.formInputs.galaxySize.on('pointerdown', () => {
            const currentIndex = sizes.indexOf(this.formInputs.selectedSize);
            const nextIndex = (currentIndex + 1) % sizes.length;
            this.formInputs.selectedSize = sizes[nextIndex];
            this.formInputs.galaxySize.setText(this.formInputs.selectedSize);
        });

        // Buttons
        const cancelButton = this.add.text(
            this.cameras.main.centerX - 100,
            500,
            'Cancel',
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#ff0000',
                backgroundColor: '#333333',
                padding: { x: 20, y: 10 }
            }
        ).setInteractive();

        const startButton = this.add.text(
            this.cameras.main.centerX + 100,
            500,
            'Start',
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#00ff00',
                backgroundColor: '#333333',
                padding: { x: 20, y: 10 }
            }
        ).setInteractive();

        // Button hover effects
        [cancelButton, startButton].forEach(button => {
            button.on('pointerover', () => {
                button.setBackgroundColor('#444444');
            });
            button.on('pointerout', () => {
                button.setBackgroundColor('#333333');
            });
        });

        // Button click handlers
        cancelButton.on('pointerdown', () => {
            this.scene.start('StartupScene');
        });

        startButton.on('pointerdown', async () => {
            try {
                const gameData = {
                    player_empire_name: this.formInputs.empireName.text,
                    computer_empire_count: parseInt(this.formInputs.computerCount.text),
                    galaxy_size: this.formInputs.selectedSize
                };

                console.log('Sending game data:', gameData);

                const response = await fetch('/api/play/games/start/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(gameData)
                });

                console.log('Response status:', response.status);

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error('API error:', errorData);
                    throw new Error(errorData.detail || 'Failed to start game');
                }

                const data = await response.json();
                console.log('Game created:', data);
                this.scene.start('GalaxyScene', data);
            } catch (error) {
                console.error('Error starting game:', error);
                this.showError(error instanceof Error ? error.message : 'Failed to start game');
            }
        });

        // Input handling
        this.formInputs.empireName.on('pointerdown', () => {
            this.currentInput = 'empireName';
            this.formInputs.empireName.setBackgroundColor('#666666');
            this.formInputs.computerCount.setBackgroundColor('#333333');
        });

        this.formInputs.computerCount.on('pointerdown', () => {
            this.currentInput = 'computerCount';
            this.formInputs.computerCount.setBackgroundColor('#666666');
            this.formInputs.empireName.setBackgroundColor('#333333');
        });

        // Keyboard input
        this.keyboard = this.input.keyboard!;
        this.keyboard.on('keydown', this.handleKeyInput, this);
    }

    private handleKeyInput(event: KeyboardEvent) {
        if (!this.currentInput) return;

        if (event.key === 'Backspace') {
            const currentText = this.formInputs[this.currentInput].text;
            if (currentText.length > 0) {
                this.formInputs[this.currentInput].setText(currentText.slice(0, -1));
            }
            return;
        }

        if (this.currentInput === 'computerCount') {
            if (event.key >= '0' && event.key <= '9') {
                const newValue = parseInt(this.formInputs.computerCount.text + event.key);
                if (newValue <= 10) { // Limit to 10 computer empires
                    this.formInputs.computerCount.setText(newValue.toString());
                }
            }
        } else if (this.currentInput === 'empireName') {
            if (event.key.length === 1) { // Single character
                const newText = this.formInputs.empireName.text + event.key;
                if (newText.length <= 20) { // Limit name length
                    this.formInputs.empireName.setText(newText);
                }
            }
        }
    }
} 