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
        ).setOrigin(0.5);

        // Add glowing effect to title
        this.tweens.add({
            targets: title,
            alpha: { from: 0.7, to: 1 },
            duration: 1500,
            ease: 'Sine.InOut',
            yoyo: true,
            repeat: -1
        });

        // Create menu items
        const createMenuItem = (text: string, y: number, callback: () => void) => {
            const menuItem = this.add.text(
                this.cameras.main.centerX,
                y,
                text,
                {
                    fontFamily: 'monospace',
                    fontSize: '32px',
                    color: '#4444ff',
                    align: 'center',
                    backgroundColor: '#000000',
                    padding: { x: 20, y: 10 }
                }
            ).setOrigin(0.5);

            menuItem.setInteractive({ useHandCursor: true });

            // Add hover effects
            menuItem.on('pointerover', () => {
                menuItem.setStyle({ color: '#8888ff' });
                this.tweens.add({
                    targets: menuItem,
                    scaleX: 1.1,
                    scaleY: 1.1,
                    duration: 100
                });
            });

            menuItem.on('pointerout', () => {
                menuItem.setStyle({ color: '#4444ff' });
                this.tweens.add({
                    targets: menuItem,
                    scaleX: 1,
                    scaleY: 1,
                    duration: 100
                });
            });

            menuItem.on('pointerdown', callback);

            this.menuItems.push(menuItem);
            return menuItem;
        };

        // Create New Game menu item
        createMenuItem('NEW GAME', this.cameras.main.height * 0.5, () => {
            this.scene.start('NewGameScene');
        });

        // Create Load Game menu item
        createMenuItem('LOAD GAME', this.cameras.main.height * 0.6, () => {
            this.scene.start('LoadGameScene');
        });

        // Debug info
        console.log('StartupScene created');
    }
} 