import Phaser from 'phaser';

export class StartupScene extends Phaser.Scene {
    private menuItems: Phaser.GameObjects.Text[];

    constructor() {
        super({ key: 'StartupScene' });
        this.menuItems = [];
    }

    preload() {
        // Preload assets if needed
    }

    create() {
        // Set black background
        this.cameras.main.setBackgroundColor('#000000');

        // Create title text with sci-fi style
        const title = this.add.text(
            this.cameras.main.centerX,
            this.cameras.main.height * 0.3,
            'SPACE CONQUEST',
            {
                fontFamily: 'monospace',
                fontSize: '48px',
                color: '#00ff00',
                align: 'center',
                stroke: '#003300',
                strokeThickness: 6
            }
        );
        title.setOrigin(0.5);

        // Add glowing effect to title
        this.tweens.add({
            targets: title,
            alpha: { from: 0.7, to: 1 },
            duration: 1500,
            ease: 'Sine.InOut',
            yoyo: true,
            repeat: -1
        });

        // Create menu item with sci-fi style
        const newGameText = this.add.text(
            this.cameras.main.centerX,
            this.cameras.main.height * 0.6,
            'NEW GAME',
            {
                fontFamily: 'monospace',
                fontSize: '32px',
                color: '#4444ff',
                align: 'center',
                backgroundColor: '#000000',
                padding: { x: 20, y: 10 }
            }
        );
        newGameText.setOrigin(0.5);
        newGameText.setInteractive({ useHandCursor: true });

        // Add hover effects
        newGameText.on('pointerover', () => {
            newGameText.setStyle({ color: '#8888ff' });
            this.tweens.add({
                targets: newGameText,
                scaleX: 1.1,
                scaleY: 1.1,
                duration: 100
            });
        });

        newGameText.on('pointerout', () => {
            newGameText.setStyle({ color: '#4444ff' });
            this.tweens.add({
                targets: newGameText,
                scaleX: 1,
                scaleY: 1,
                duration: 100
            });
        });

        newGameText.on('pointerdown', () => {
            this.scene.start('NewGameScene');
        });

        this.menuItems.push(newGameText);

        // Debug info
        console.log('StartupScene created');
    }
} 