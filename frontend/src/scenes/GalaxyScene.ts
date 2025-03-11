import Phaser from 'phaser';
import Button from '../ui/Button';
import Panel, { PanelConfig } from '../ui/Panel';
import { TextStyles } from '../ui/TextStyles';
import { useGameState } from '../state/GameState';
import type { StarSystem } from '../state/GameState';

interface ButtonConfig {
    scene: Phaser.Scene;
    x: number;
    y: number;
    text: string;
    callback: () => void;
}

export default class GalaxyScene extends Phaser.Scene {
    private systems: StarSystem[] = [];
    private infoPanel: Panel | null = null;

    constructor() {
        super('GalaxyScene');
    }

    preload() {
        // Preload assets here
    }

    create() {
        const { height } = this.cameras.main;
        const gameState = useGameState.getState();

        // Check if we have a game state
        if (!gameState.gameId) {
            console.error('No game state found, returning to startup scene');
            this.scene.start('StartupScene');
            return;
        }

        this.systems = gameState.systems;

        // Draw systems
        this.systems.forEach(system => {
            const star = this.add.circle(system.x, system.y, system.size, system.color);
            star.setInteractive();

            star.on('pointerover', () => this.onSystemHover(system));
            star.on('pointerout', () => this.onSystemOut());
            star.on('pointerdown', () => this.onSystemClick(system));
        });

        // Add UI elements
        const buttonConfig: ButtonConfig = {
            scene: this,
            x: 10,
            y: height - 40,
            text: 'Back to Menu',
            callback: () => this.backToMenu()
        };
        new Button(buttonConfig);
    }

    private onSystemHover(system: StarSystem): void {
        if (this.infoPanel) {
            this.infoPanel.destroy();
        }

        const panelConfig: PanelConfig = {
            scene: this,
            x: 10,
            y: 10,
            width: 200,
            height: 150,
            title: system.name,
            backgroundColor: 0x000000,
            backgroundAlpha: 0.8,
            borderColor: 0x4a6fa5,
            borderWidth: 2,
            cornerRadius: 8
        };
        
        this.infoPanel = new Panel(panelConfig);
        this.infoPanel.addContent([
            this.add.text(0, 0, `Type: ${this.getStarType(system)}`, TextStyles.normal),
            this.add.text(0, 20, `Planets: ${system.planets}`, TextStyles.normal),
            this.add.text(0, 40, `Discovery Level: ${system.discoveryLevel}`, TextStyles.normal),
            this.add.text(0, 60, system.explored ? 'Explored' : 'Unexplored', TextStyles.normal)
        ]);
    }

    private onSystemOut(): void {
        if (this.infoPanel) {
            this.infoPanel.destroy();
            this.infoPanel = null;
        }
    }

    private onSystemClick(system: StarSystem): void {
        const gameState = useGameState.getState();
        gameState.selectSystem(system);
        this.scene.start('SystemScene');
    }

    private getStarType(system: StarSystem): string {
        // Simplified star type based on color
        const colors: Record<number, string> = {
            0xff0000: 'Red Dwarf',
            0xffff00: 'Yellow Star',
            0xffffff: 'White Star',
            0x0000ff: 'Blue Giant'
        };
        return colors[system.color] || 'Unknown';
    }

    private backToMenu(): void {
        this.scene.start('StartupScene');
    }
}
