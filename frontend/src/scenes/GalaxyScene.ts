import Phaser from 'phaser';
import Button from '../ui/Button';
import Panel from '../ui/Panel';
import { TextStyles } from '../ui/TextStyles';
import api from '../utils/api';

interface StarSystem {
    id: string;
    name: string;
    x: number;
    y: number;
    size: number;
    color: number;
    explored: boolean;
    planets: number;
    discoveryLevel: number; // 0: visible light, 1-5: scanning levels, 6: visited
}

export default class GalaxyScene extends Phaser.Scene {
    private systems: StarSystem[] = [];
    private selectedSystem: StarSystem | null = null;
    private infoPanel: Panel | null = null;

    constructor() {
        super('GalaxyScene');
    }

    preload() {
        // Preload assets here
    }

    create() {
        const { width, height } = this.cameras.main;
        const gameState = api.GameState;

        console.log('GalaxyScene create - Current game state:', {
            gameId: gameState.gameId,
            playerName: gameState.playerName,
            playerEmpire: gameState.playerEmpire,
            resources: gameState.resources,
            galaxySize: gameState.galaxySize,
            galaxySystems: gameState.galaxySystems,
            galaxyExplored: gameState.galaxyExplored,
            turn: gameState.turn
        });

        // Check if we have a game state
        if (!gameState.gameId) {
            console.error('No game state found, returning to startup scene');
            this.scene.start('StartupScene');
            return;
        }

        // Title
        this.add.text(
            width / 2,
            30,
            'Galaxy View',
            TextStyles.subtitle
        ).setOrigin(0.5);

        // Player info panel
        const playerPanel = new Panel({
            scene: this,
            x: 150,
            y: 80,
            width: 280,
            height: 120,
            title: gameState.playerName || 'Player'
        });

        // Add player resources
        if (gameState.resources) {
            console.log('Player resources:', gameState.resources);
            
            // Check if resources properties exist
            const credits = gameState.resources.credits !== undefined ? gameState.resources.credits : 0;
            const minerals = gameState.resources.mineral !== undefined ? gameState.resources.mineral : 0;
            const energy = gameState.resources.energy !== undefined ? gameState.resources.energy : 0;
            
            const resourcesText = this.add.text(
                0,
                -20,
                `Credits: ${credits}\nMinerals: ${minerals}\nEnergy: ${energy}`,
                TextStyles.resource
            ).setOrigin(0.5, 0);
            
            playerPanel.addContent(resourcesText);
        } else {
            console.error('No resources found in game state');
            
            // Add default resources text
            const resourcesText = this.add.text(
                0,
                -20,
                'Credits: 0\nMinerals: 0\nEnergy: 0',
                TextStyles.resource
            ).setOrigin(0.5, 0);
            
            playerPanel.addContent(resourcesText);
        }

        // Generate star systems from game state
        this.generateStarSystems();

        // Create star systems
        this.systems.forEach(system => {
            // Use different colors based on discovery level
            let color = 0x444444; // Default for visible light only
            
            if (system.discoveryLevel === 6) {
                color = 0xffff00; // Visited systems are bright yellow
            } else if (system.discoveryLevel >= 1 && system.discoveryLevel <= 5) {
                // Scanning levels 1-5 have progressively brighter colors
                const brightness = 0x444444 + (0x111111 * system.discoveryLevel);
                color = brightness;
            }
            
            const star = this.add.circle(system.x, system.y, system.size, color);
            star.setInteractive({ useHandCursor: true })
                .on('pointerover', () => this.onSystemHover(system))
                .on('pointerout', () => this.onSystemOut())
                .on('pointerdown', () => this.onSystemClick(system));
            
            // Always display the system name
            this.add.text(
                system.x,
                system.y + system.size + 10,
                system.name,
                TextStyles.small
            ).setOrigin(0.5);
        });

        // Back button
        new Button({
            scene: this,
            x: 100,
            y: height - 50,
            text: 'Back to Menu',
            textStyle: TextStyles.button,
            callback: () => this.backToMenu()
        });

        // Turn indicator
        this.add.text(
            width - 20,
            20,
            `Turn: ${gameState.turn || 1}`,
            TextStyles.normal
        ).setOrigin(1, 0);

        // Galaxy info
        this.add.text(
            width - 20,
            50,
            `Galaxy Size: ${gameState.galaxySize || 'Medium'}\nSystems: ${gameState.galaxySystems || 0}\nExplored: ${gameState.galaxyExplored || 0}`,
            TextStyles.small
        ).setOrigin(1, 0);
    }

    private generateStarSystems(): void {
        // Clear existing systems
        this.systems = [];
        
        const { width, height } = this.cameras.main;
        const padding = 100; // Padding from edges
        
        // Get game state
        const gameState = api.GameState;
        
        // If we don't have a game state, generate some dummy systems
        if (!gameState.gameId) {
            // Star colors
            const colors = [0xffff00, 0xff8800, 0xff0000, 0x8888ff, 0xffffff];
            
            // Generate systems
            for (let i = 0; i < 15; i++) {
                // Determine discovery level: 0 for all systems (visible light), 
                // higher levels for some systems
                let discoveryLevel = 0; // Default: visible light
                if (i < 3) {
                    discoveryLevel = 6; // Visited
                } else if (i < 6) {
                    discoveryLevel = Phaser.Math.Between(1, 5); // Scanning levels 1-5
                }
                
                const system: StarSystem = {
                    id: `dummy-${i}`,
                    name: `System ${i + 1}`,
                    x: Phaser.Math.Between(padding, width - padding),
                    y: Phaser.Math.Between(padding, height - padding),
                    size: Phaser.Math.Between(3, 8),
                    color: colors[Phaser.Math.Between(0, colors.length - 1)],
                    explored: i < 3, // First 3 systems are explored
                    planets: Phaser.Math.Between(1, 8),
                    discoveryLevel: discoveryLevel
                };
                
                this.systems.push(system);
            }
            return;
        }
        
        // In a real implementation, we would get the star systems from the backend
        // For now, we'll generate random systems based on the galaxy size
        const systemCount = gameState.galaxySystems || 20;
        
        // Generate systems
        for (let i = 0; i < systemCount; i++) {
            // Calculate position based on a circular galaxy
            const radius = Math.sqrt(Math.random()) * (Math.min(width, height) / 2 - padding);
            const angle = Math.random() * Math.PI * 2;
            const x = width / 2 + radius * Math.cos(angle);
            const y = height / 2 + radius * Math.sin(angle);
            
            // Determine discovery level
            let discoveryLevel = 0; // Default: visible light
            if (i === 0) {
                discoveryLevel = 6; // First system is visited
            } else if (i < 3) {
                discoveryLevel = Phaser.Math.Between(1, 5); // Some systems have scanning data
            }
            
            const system: StarSystem = {
                id: `system-${i}`,
                name: `System ${i + 1}`,
                x: x,
                y: y,
                size: Phaser.Math.Between(3, 8),
                color: 0xffff00, // Will be overridden based on explored status
                explored: i === 0, // Only the first system is explored initially
                planets: Phaser.Math.Between(1, 8),
                discoveryLevel: discoveryLevel
            };
            
            this.systems.push(system);
        }
    }

    private onSystemHover(system: StarSystem): void {
        // Always show system name in a tooltip
        const tooltip = this.add.text(
            system.x,
            system.y - system.size - 20,
            system.name,
            TextStyles.normal
        ).setOrigin(0.5);
        
        // Store reference to remove on pointer out
        (this as any).tooltip = tooltip;
    }

    private onSystemOut(): void {
        // Remove tooltip
        if ((this as any).tooltip) {
            (this as any).tooltip.destroy();
            (this as any).tooltip = null;
        }
    }

    private onSystemClick(system: StarSystem): void {
        this.selectedSystem = system;
        
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
            y: height / 2,
            width: 250,
            height: 300,
            title: system.name,
            draggable: true
        });
        
        // Always add a View System button
        const viewButton = new Button({
            scene: this,
            x: 0,
            y: 50,
            text: 'View System',
            textStyle: TextStyles.button,
            callback: () => this.viewSystem(system)
        });
        
        this.infoPanel.addContent(viewButton);
        
        // Add system info based on discovery level
        let infoText = '';
        
        if (system.discoveryLevel === 0) {
            infoText = 'Status: Visible Light Only\nNo detailed data available';
        } else if (system.discoveryLevel >= 1 && system.discoveryLevel <= 5) {
            infoText = `Status: Scan Level ${system.discoveryLevel}\nPlanets: ${system.planets}`;
            
            // Add more details as scan level increases
            if (system.discoveryLevel >= 3) {
                infoText += `\nStar Type: ${this.getStarType(system)}`;
            }
            if (system.discoveryLevel >= 4) {
                infoText += `\nResources: ${this.getResourceLevel()}`;
            }
            if (system.discoveryLevel >= 5) {
                infoText += `\nThreat Level: ${this.getThreatLevel()}`;
            }
        } else if (system.discoveryLevel === 6) {
            infoText = `Status: Visited\nPlanets: ${system.planets}\nStar Type: ${this.getStarType(system)}\nResources: ${this.getResourceLevel()}\nThreat Level: ${this.getThreatLevel()}`;
        }
        
        const info = this.add.text(
            0,
            -50,
            infoText,
            TextStyles.normal
        ).setOrigin(0.5, 0);
        
        this.infoPanel.addContent(info);
        
        // Add explore button for unexplored systems
        if (!system.explored) {
            const exploreButton = new Button({
                scene: this,
                x: 0,
                y: 100,
                text: 'Explore System',
                textStyle: TextStyles.button,
                callback: () => this.exploreSystem(system)
            });
            
            this.infoPanel.addContent(exploreButton);
        }
    }
    
    private getStarType(system: StarSystem): string {
        // Determine star type based on system ID for consistency
        const types = ['G-class', 'K-class', 'M-class', 'F-class', 'A-class', 'B-class', 'O-class'];
        const typeIndex = parseInt(system.id.split('-')[1]) % types.length;
        return types[typeIndex];
    }
    
    private exploreSystem(system: StarSystem): void {
        console.log(`Exploring system ${system.id}`);
        
        // In a real implementation, we would call the backend to explore the system
        // For now, we'll just mark it as explored and increase discovery level
        system.explored = true;
        system.discoveryLevel = 6; // Set to visited (highest level)
        
        // Refresh the scene to update the display
        this.scene.restart();
    }
    
    private getResourceLevel(): string {
        const levels = ['Low', 'Medium', 'High'];
        return levels[Phaser.Math.Between(0, 2)];
    }
    
    private getThreatLevel(): string {
        const levels = ['None', 'Low', 'Medium', 'High'];
        return levels[Phaser.Math.Between(0, 3)];
    }

    private viewSystem(system: StarSystem): void {
        console.log(`Viewing system ${system.name} with discovery level ${system.discoveryLevel}`);
        this.scene.start('SystemScene', { 
            systemId: system.id,
            discoveryLevel: system.discoveryLevel
        });
    }

    private backToMenu(): void {
        this.scene.start('StartupScene');
    }
}
