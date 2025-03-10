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

export default class SystemScene extends Phaser.Scene {
    private planets: Planet[] = [];
    private infoPanel: Panel | null = null;

    constructor() {
        super('SystemScene');
    }

    preload() {
        // Preload assets here
    }

    create() {
        const { width, height } = this.cameras.main;
        const gameState = useGameState.getState();
        const selectedSystem = gameState.selectedSystem;

        if (!selectedSystem) {
            console.error('No system selected, returning to galaxy view');
            this.scene.start('GalaxyScene');
            return;
        }

        // Add system name
        this.add.text(width / 2, 30, selectedSystem.name, TextStyles.title)
            .setOrigin(0.5);

        // Create orbit circles
        const orbitRadii = [100, 150, 200, 250, 300];
        orbitRadii.forEach(radius => {
            this.add.circle(width / 2, height / 2, radius * 2)
                .setStrokeStyle(1, 0x444444);
        });

        // Add star at center
        this.add.circle(width / 2, height / 2, 20, selectedSystem.color);

        // Create planets
        const planetPositions = this.calculatePlanetPositions(
            selectedSystem.planets,
            width / 2,
            height / 2,
            orbitRadii
        );

        planetPositions.forEach((pos, index) => {
            const planet = this.add.circle(pos.x, pos.y, 10, 0x00ff00);
            planet.setInteractive();

            planet.on('pointerover', () => this.onPlanetHover(gameState.planets[index]));
            planet.on('pointerout', () => this.onPlanetOut());
            planet.on('pointerdown', () => this.onPlanetClick(gameState.planets[index]));
        });

        // Add back button
        const buttonConfig: ButtonConfig = {
            scene: this,
            x: 10,
            y: height - 40,
            text: 'Back to Galaxy',
            callback: () => this.backToGalaxy()
        };
        new Button(buttonConfig);
    }

    private calculatePlanetPositions(
        planetCount: number,
        centerX: number,
        centerY: number,
        orbitRadii: number[]
    ): { x: number; y: number }[] {
        const positions: { x: number; y: number }[] = [];
        let orbitIndex = 0;

        for (let i = 0; i < planetCount; i++) {
            if (orbitIndex >= orbitRadii.length) break;

            const angle = (Math.PI * 2 * i) / Math.min(planetCount, 3);
            const radius = orbitRadii[orbitIndex];

            positions.push({
                x: centerX + Math.cos(angle) * radius,
                y: centerY + Math.sin(angle) * radius
            });

            if ((i + 1) % 3 === 0) orbitIndex++;
        }

        return positions;
    }

    private onPlanetHover(planet: Planet): void {
        if (this.infoPanel) {
            this.infoPanel.destroy();
        }

        const panelConfig: PanelConfig = {
            scene: this,
            x: 10,
            y: 10,
            width: 200,
            height: 180,
            title: planet.name,
            backgroundColor: 0x000000,
            backgroundAlpha: 0.8,
            borderColor: 0x4a6fa5,
            borderWidth: 2,
            cornerRadius: 8
        };
        
        this.infoPanel = new Panel(panelConfig);
        this.infoPanel.addContent([
            this.add.text(0, 0, `Type: ${planet.type}`, TextStyles.normal),
            this.add.text(0, 20, `Size: ${planet.size}`, TextStyles.normal),
            this.add.text(0, 40, 'Resources:', TextStyles.normal),
            this.add.text(0, 60, `  Minerals: ${planet.resources.minerals}`, TextStyles.normal),
            this.add.text(0, 80, `  Energy: ${planet.resources.energy}`, TextStyles.normal),
            this.add.text(0, 100, `  Organics: ${planet.resources.organics}`, TextStyles.normal),
            this.add.text(0, 120, planet.colonized ? 'Colonized' : 'Uncolonized', TextStyles.normal)
        ]);
    }

    private onPlanetOut(): void {
        if (this.infoPanel) {
            this.infoPanel.destroy();
            this.infoPanel = null;
        }
    }

    private onPlanetClick(planet: Planet): void {
        const gameState = useGameState.getState();
        gameState.selectPlanet(planet);
        this.scene.start('PlanetScene');
    }

    private backToGalaxy(): void {
        this.scene.start('GalaxyScene');
    }
}
