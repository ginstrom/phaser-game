import Phaser from 'phaser';

export default class MainScene extends Phaser.Scene {
    constructor() {
        super('MainScene');
    }

    preload() {
        // Preload assets here
    }

    create() {
        // Create game objects here
        this.add.text(
            this.cameras.main.centerX,
            this.cameras.main.centerY,
            '4X Space Empire Game',
            {
                color: '#ffffff',
                fontSize: '32px'
            }
        ).setOrigin(0.5);
    }

    update() {
        // Update game objects here
    }
}
