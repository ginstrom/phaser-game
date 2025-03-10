import Phaser from 'phaser';
import Button from '../ui/Button';
import Panel, { PanelConfig } from '../ui/Panel';
import { TextStyles } from '../ui/TextStyles';
import { useGameState } from '../state/GameState';
import type { Planet } from '../state/GameState';

interface ButtonConfig {
    scene: Phaser.Scene;
    x: number;
    y: number;
    text: string;
    callback: () => void;
}

export default class PlanetScene extends Phaser.Scene {
    private infoPanel: Panel | null = null;

    constructor() {
        super('PlanetScene');
    }

    preload() {
        // Preload assets here
    }

    create() {
        const { width, height } = this.cameras.main;
        const gameState = useGameState.getState();
        const selectedPlanet = gameState.selectedPlanet;

        if (!selectedPlanet) {
            console.error('No planet selected, returning to system view');
            this.scene.start('SystemScene');
            return;
        }

        // Add planet name
        this.add.text(width / 2, 30, selectedPlanet.name, TextStyles.title)
            .setOrigin(0.5);

        // Draw planet
        const planetSize = Math.min(width, height) * 0.3;
        this.add.circle(width / 2, height / 2, planetSize, this.getPlanetColor(selectedPlanet.type));

        // Add planet info panel
        const panelConfig: PanelConfig = {
            scene: this,
            x: 10,
            y: 10,
            width: 250,
            height: 300,
            title: 'Planet Information',
            backgroundColor: 0x000000,
            backgroundAlpha: 0.8,
            borderColor: 0x4a6fa5,
            borderWidth: 2,
            cornerRadius: 8
        };
        
        this.infoPanel = new Panel(panelConfig);
        this.infoPanel.addContent([
            this.add.text(0, 0, `Type: ${selectedPlanet.type}`, TextStyles.normal),
            this.add.text(0, 30, `Size: ${selectedPlanet.size}`, TextStyles.normal),
            this.add.text(0, 60, 'Resources:', TextStyles.normal),
            this.add.text(0, 90, `  Minerals: ${selectedPlanet.resources.minerals}`, TextStyles.normal),
            this.add.text(0, 120, `  Energy: ${selectedPlanet.resources.energy}`, TextStyles.normal),
            this.add.text(0, 150, `  Organics: ${selectedPlanet.resources.organics}`, TextStyles.normal),
            this.add.text(0, 180, selectedPlanet.colonized ? 'Status: Colonized' : 'Status: Uncolonized', TextStyles.normal)
        ]);

        if (!selectedPlanet.colonized) {
            const colonizeButtonConfig: ButtonConfig = {
                scene: this,
                x: width - 150,
                y: height - 100,
                text: 'Colonize Planet',
                callback: () => this.colonizePlanet(selectedPlanet)
            };
            new Button(colonizeButtonConfig);
        }

        // Add back button
        const backButtonConfig: ButtonConfig = {
            scene: this,
            x: 10,
            y: height - 40,
            text: 'Back to System',
            callback: () => this.backToSystem()
        };
        new Button(backButtonConfig);
    }

    private getPlanetColor(type: string): number {
        const colors: Record<string, number> = {
            'Rocky': 0x8B4513,
            'Gas Giant': 0xFFA500,
            'Ice': 0xADD8E6,
            'Terrestrial': 0x228B22,
            'Desert': 0xF4A460
        };
        return colors[type] || 0x808080;
    }

    private colonizePlanet(planet: Planet): void {
        // In a real implementation, this would call the backend
        const gameState = useGameState.getState();
        const updatedPlanet = { ...planet, colonized: true };
        gameState.selectPlanet(updatedPlanet);
        
        // Refresh the scene
        this.scene.restart();
    }

    private backToSystem(): void {
        this.scene.start('SystemScene');
    }
}
