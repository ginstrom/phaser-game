import Phaser from 'phaser';
import Button from '../ui/Button';
import { TextStyles } from '../ui/TextStyles';

export default class StartupScene extends Phaser.Scene {
    constructor() {
        super('StartupScene');
    }

    preload() {
        // Preload assets here
        // In a real game, we would load images, sounds, etc.
    }

    create() {
        const { width, height } = this.cameras.main;
        
        // Title
        this.add.text(
            width / 2,
            height * 0.2,
            '4X Space Empire',
            TextStyles.title
        ).setOrigin(0.5);

        // Subtitle
        this.add.text(
            width / 2,
            height * 0.3,
            'A Turn-Based Strategy Game',
            TextStyles.subtitle
        ).setOrigin(0.5);

        // Create buttons
        const buttonSpacing = 70;
        const startY = height * 0.5;

        // New Game button
        new Button({
            scene: this,
            x: width / 2,
            y: startY,
            text: 'New Game',
            textStyle: TextStyles.button,
            callback: () => this.startNewGame()
        });

        // Load Game button
        new Button({
            scene: this,
            x: width / 2,
            y: startY + buttonSpacing,
            text: 'Load Game',
            textStyle: TextStyles.button,
            callback: () => this.loadGame()
        });

        // Settings button
        new Button({
            scene: this,
            x: width / 2,
            y: startY + buttonSpacing * 2,
            text: 'Settings',
            textStyle: TextStyles.button,
            callback: () => this.openSettings()
        });

        // Exit button
        new Button({
            scene: this,
            x: width / 2,
            y: startY + buttonSpacing * 3,
            text: 'Exit',
            textStyle: TextStyles.button,
            callback: () => this.exitGame()
        });

        // Version text
        this.add.text(
            width - 20,
            height - 20,
            'Version 0.1.0',
            TextStyles.small
        ).setOrigin(1);
    }

    private startNewGame(): void {
        console.log('Starting new game');
        this.scene.start('GalaxyScene');
    }

    private loadGame(): void {
        console.log('Load game functionality not implemented yet');
        // In a real game, this would open a load game dialog
    }

    private openSettings(): void {
        console.log('Settings functionality not implemented yet');
        // In a real game, this would open a settings dialog
    }

    private exitGame(): void {
        console.log('Exit game');
        // In a browser, we can't really exit the game, but we could show a confirmation dialog
    }
}
