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
    private discoveryLevel: number = 0; // 0: visible light, 1-5: scanning levels, 6: visited
    private planets: Planet[] = [];
    private selectedPlanet: Planet | null = null;
    private infoPanel: Panel | null = null;
    private orbitGraphics: Phaser.GameObjects.Graphics | null = null;

    constructor() {
        super('SystemScene');
    }

    init(data: { systemId: number, discoveryLevel?: number }) {
        this.systemId = data.systemId;
        this.systemName = `System ${this.systemId + 1}`;
        this.discoveryLevel = data.discoveryLevel || 0;
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
        
        // Draw orbits and planets based on discovery level
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

        // System info panel with details based on discovery level
        const systemInfoPanel = new Panel({
            scene: this,
            x: width - 150,
            y: 100,
            width: 250,
            height: 150,
            title: 'System Info'
        });

        // Determine what information to show based on discovery level
        let infoText = '';
        
        // At minimum, show star details and number of planets/orbits
        infoText = `Star Type: ${this.getStarType()}\nPlanets: ${this.planets.length}`;
        
        // Add more details as discovery level increases
        if (this.discoveryLevel >= 2) {
            infoText += `\nAsteroids: ${this.hasAsteroids() ? 'Yes' : 'No'}`;
        }
        
        if (this.discoveryLevel >= 3) {
            infoText += `\nStability: ${this.getSystemStability()}`;
        }
        
        if (this.discoveryLevel >= 4) {
            infoText += `\nResources: ${this.getSystemResourceLevel()}`;
        }
        
        if (this.discoveryLevel >= 5) {
            infoText += `\nSpecial Features: ${this.getSpecialFeatures()}`;
        }
        
        const systemInfo = this.add.text(
            0,
            0,
            infoText,
            TextStyles.normal
        ).setOrigin(0.5);

        systemInfoPanel.addContent(systemInfo);
        
        // Add discovery level indicator
        this.add.text(
            width - 20,
            20,
            `Discovery Level: ${this.getDiscoveryLevelText()}`,
            TextStyles.small
        ).setOrigin(1, 0);
    }
    
    private getDiscoveryLevelText(): string {
        const levels = [
            'Visible Light Only',
            'Scan Level 1',
            'Scan Level 2',
            'Scan Level 3',
            'Scan Level 4',
            'Scan Level 5',
            'Visited'
        ];
        return levels[this.discoveryLevel];
    }
    
    private getStarType(): string {
        // Determine star type based on system ID for consistency
        const types = ['G-class', 'K-class', 'M-class', 'F-class', 'A-class', 'B-class', 'O-class'];
        const typeIndex = this.systemId % types.length;
        return types[typeIndex];
    }
    
    private hasAsteroids(): boolean {
        // Determine if system has asteroids based on system ID
        return this.systemId % 3 === 0;
    }
    
    private getSystemStability(): string {
        // Determine system stability based on system ID
        const stability = ['Unstable', 'Moderate', 'Stable', 'Very Stable'];
        return stability[this.systemId % stability.length];
    }
    
    private getSystemResourceLevel(): string {
        // Determine system resource level based on system ID
        const resources = ['Poor', 'Average', 'Rich', 'Abundant'];
        return resources[this.systemId % resources.length];
    }
    
    private getSpecialFeatures(): string {
        // Determine special features based on system ID
        const features = ['None', 'Nebula', 'Black Hole', 'Neutron Star', 'Wormhole'];
        return features[this.systemId % features.length];
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
        
        // Draw orbits and planets based on discovery level
        this.planets.forEach((planet, index) => {
            // Calculate orbit radius
            const radius = minRadius + index * radiusStep;
            
            // Always draw orbits at minimum
            if (this.orbitGraphics) {
                this.orbitGraphics.strokeCircle(centerX, centerY, radius);
            }
            
            // Calculate planet position on orbit
            const angle = Phaser.Math.Between(0, 360) * Math.PI / 180;
            planet.x = centerX + radius * Math.cos(angle);
            planet.y = centerY + radius * Math.sin(angle);
            
            // Draw planets with varying detail based on discovery level
            let planetColor = 0x444444; // Default dark color for low discovery levels
            let planetVisible = true;
            
            if (this.discoveryLevel === 0) {
                // At visible light level, only show orbits, not planets
                planetVisible = false;
            } else if (this.discoveryLevel >= 1 && this.discoveryLevel <= 3) {
                // At low scan levels, show planets as simple dots
                planetColor = 0x888888;
            } else if (this.discoveryLevel >= 4) {
                // At higher scan levels, show planets with their actual colors
                planetColor = planet.color;
            }
            
            if (planetVisible) {
                // Draw planet
                const planetCircle = this.add.circle(planet.x, planet.y, planet.size, planetColor);
                
                // Make planet interactive
                planetCircle.setInteractive({ useHandCursor: true })
                    .on('pointerover', () => this.onPlanetHover(planet))
                    .on('pointerout', () => this.onPlanetOut())
                    .on('pointerdown', () => this.onPlanetClick(planet));
                
                // Add colonized indicator if applicable and discovery level is high enough
                if (planet.colonized && this.discoveryLevel >= 5) {
                    this.add.rectangle(planet.x, planet.y - planet.size - 5, 10, 10, 0x00ff00);
                }
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
        
        // Always add View Planet button
        const viewButton = new Button({
            scene: this,
            x: 0,
            y: 100,
            text: 'View Planet',
            textStyle: TextStyles.button,
            callback: () => this.viewPlanet(planet)
        });
        
        this.infoPanel.addContent(viewButton);
        
        // Add planet info based on discovery level
        let infoText = '';
        
        if (this.discoveryLevel <= 2) {
            // At low discovery levels, only show basic info
            infoText = 'Limited data available';
        } else if (this.discoveryLevel === 3) {
            // At medium discovery level, show planet type
            infoText = `Type: ${planet.type}\nSize: ${planet.size * 1000} km`;
        } else if (this.discoveryLevel === 4) {
            // At higher discovery level, add resources
            infoText = `Type: ${planet.type}\nSize: ${planet.size * 1000} km\nResources: ${planet.resources}`;
        } else if (this.discoveryLevel >= 5) {
            // At highest discovery levels, show all info
            infoText = `Type: ${planet.type}\nSize: ${planet.size * 1000} km\nResources: ${planet.resources}\nColonized: ${planet.colonized ? 'Yes' : 'No'}`;
        }
        
        const info = this.add.text(
            0,
            -50,
            infoText,
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
