import Phaser from 'phaser';
import Button from '../ui/Button';
import Panel from '../ui/Panel';
import { TextStyles } from '../ui/TextStyles';

interface Planet {
    id: number;
    name: string;
    x: number;
    y: number;
    size: number;
    color: number;
    type: string;
    resources: string;
    colonized: boolean;
}

export default class SystemScene extends Phaser.Scene {
    private systemId: number = 0;
    private systemName: string = '';
    private planets: Planet[] = [];
    private selectedPlanet: Planet | null = null;
    private infoPanel: Panel | null = null;
    private orbitGraphics: Phaser.GameObjects.Graphics | null = null;

    constructor() {
        super('SystemScene');
    }

    init(data: { systemId: number }) {
        this.systemId = data.systemId;
        this.systemName = `System ${this.systemId + 1}`;
    }

    preload() {
        // Preload assets here
    }

    create() {
        const { width, height } = this.cameras.main;
        
        // Title
        this.add.text(
            width / 2,
            30,
            `${this.systemName} - System View`,
            TextStyles.subtitle
        ).setOrigin(0.5);

        // Create graphics for orbits
        this.orbitGraphics = this.add.graphics();
        this.orbitGraphics.lineStyle(1, 0x444444);

        // Create star in the center
        const starSize = 20;
        const star = this.add.circle(width / 2, height / 2, starSize, 0xffff00);
        
        // Generate planets
        this.generatePlanets();
        
        // Draw orbits and planets
        this.drawOrbitsAndPlanets();

        // Back button
        new Button({
            scene: this,
            x: 100,
            y: height - 50,
            text: 'Back to Galaxy',
            textStyle: TextStyles.button,
            callback: () => this.backToGalaxy()
        });

        // System info
        const systemInfoPanel = new Panel({
            scene: this,
            x: width - 150,
            y: 100,
            width: 250,
            height: 150,
            title: 'System Info'
        });

        const systemInfo = this.add.text(
            0,
            0,
            `Star Type: G-class\nPlanets: ${this.planets.length}\nAsteroids: Yes\nStability: Stable`,
            TextStyles.normal
        ).setOrigin(0.5);

        systemInfoPanel.addContent(systemInfo);
    }

    private generatePlanets(): void {
        // Planet types
        const types = ['Rocky', 'Gas Giant', 'Ice', 'Terrestrial', 'Desert'];
        const resources = ['Poor', 'Average', 'Rich', 'Abundant'];
        const colors = [0x888888, 0x8888ff, 0x88ff88, 0xff8888, 0xffff88];
        
        // Number of planets (3-7)
        const planetCount = Phaser.Math.Between(3, 7);
        
        for (let i = 0; i < planetCount; i++) {
            const planet: Planet = {
                id: i,
                name: `Planet ${String.fromCharCode(65 + i)}`, // A, B, C, etc.
                x: 0, // Will be set in drawOrbitsAndPlanets
                y: 0, // Will be set in drawOrbitsAndPlanets
                size: Phaser.Math.Between(5, 15),
                color: colors[Phaser.Math.Between(0, colors.length - 1)],
                type: types[Phaser.Math.Between(0, types.length - 1)],
                resources: resources[Phaser.Math.Between(0, resources.length - 1)],
                colonized: Phaser.Math.Between(0, 10) > 7 // 30% chance of being colonized
            };
            
            this.planets.push(planet);
        }
    }

    private drawOrbitsAndPlanets(): void {
        const { width, height } = this.cameras.main;
        const centerX = width / 2;
        const centerY = height / 2;
        
        // Minimum and maximum orbit radius
        const minRadius = 60;
        const maxRadius = Math.min(width, height) / 2 - 100;
        const radiusStep = (maxRadius - minRadius) / (this.planets.length - 1 || 1);
        
        // Draw orbits and planets
        this.planets.forEach((planet, index) => {
            // Calculate orbit radius
            const radius = minRadius + index * radiusStep;
            
            // Draw orbit
            if (this.orbitGraphics) {
                this.orbitGraphics.strokeCircle(centerX, centerY, radius);
            }
            
            // Calculate planet position on orbit
            const angle = Phaser.Math.Between(0, 360) * Math.PI / 180;
            planet.x = centerX + radius * Math.cos(angle);
            planet.y = centerY + radius * Math.sin(angle);
            
            // Draw planet
            const planetCircle = this.add.circle(planet.x, planet.y, planet.size, planet.color);
            
            // Make planet interactive
            planetCircle.setInteractive({ useHandCursor: true })
                .on('pointerover', () => this.onPlanetHover(planet))
                .on('pointerout', () => this.onPlanetOut())
                .on('pointerdown', () => this.onPlanetClick(planet));
            
            // Add colonized indicator if applicable
            if (planet.colonized) {
                this.add.rectangle(planet.x, planet.y - planet.size - 5, 10, 10, 0x00ff00);
            }
        });
    }

    private onPlanetHover(planet: Planet): void {
        // Show planet name in a tooltip
        const tooltip = this.add.text(
            planet.x,
            planet.y - planet.size - 20,
            planet.name,
            TextStyles.normal
        ).setOrigin(0.5);
        
        // Store reference to remove on pointer out
        (this as any).tooltip = tooltip;
    }

    private onPlanetOut(): void {
        // Remove tooltip
        if ((this as any).tooltip) {
            (this as any).tooltip.destroy();
            (this as any).tooltip = null;
        }
    }

    private onPlanetClick(planet: Planet): void {
        this.selectedPlanet = planet;
        
        // Remove existing info panel if any
        if (this.infoPanel) {
            this.infoPanel.destroy();
            this.infoPanel = null;
        }
        
        // Create info panel
        const { width, height } = this.cameras.main;
        this.infoPanel = new Panel({
            scene: this,
            x: width - 150,
            y: height / 2 + 100,
            width: 250,
            height: 300,
            title: planet.name,
            draggable: true
        });
        
        // Add content to panel
        const viewButton = new Button({
            scene: this,
            x: 0,
            y: 100,
            text: 'View Planet',
            textStyle: TextStyles.button,
            callback: () => this.viewPlanet(planet)
        });
        
        this.infoPanel.addContent(viewButton);
        
        // Add planet info
        const info = this.add.text(
            0,
            -50,
            `Type: ${planet.type}\nResources: ${planet.resources}\nColonized: ${planet.colonized ? 'Yes' : 'No'}\nSize: ${planet.size * 1000} km`,
            TextStyles.normal
        ).setOrigin(0.5, 0);
        
        this.infoPanel.addContent(info);
    }

    private viewPlanet(planet: Planet): void {
        console.log(`Viewing planet ${planet.name}`);
        this.scene.start('PlanetScene', { 
            systemId: this.systemId,
            planetId: planet.id
        });
    }

    private backToGalaxy(): void {
        this.scene.start('GalaxyScene');
    }
}
