import Phaser from 'phaser';
import Button from '../ui/Button';
import Panel from '../ui/Panel';
import { TextStyles } from '../ui/TextStyles';

interface Building {
    id: number;
    name: string;
    type: string;
    level: number;
    production: string;
    maintenance: number;
}

interface Resource {
    name: string;
    amount: number;
    production: number;
    icon?: string;
}

export default class PlanetScene extends Phaser.Scene {
    private systemId: number = 0;
    private planetId: number = 0;
    private systemName: string = '';
    private planetName: string = '';
    private buildings: Building[] = [];
    private resources: Resource[] = [];
    private planetType: string = 'Terrestrial';
    private isColonized: boolean = false;

    constructor() {
        super('PlanetScene');
    }

    init(data: { systemId: number; planetId: number }) {
        this.systemId = data.systemId;
        this.planetId = data.planetId;
        this.systemName = `System ${this.systemId + 1}`;
        this.planetName = `Planet ${String.fromCharCode(65 + this.planetId)}`;
        
        // Randomly determine if planet is colonized (70% chance if it's the first planet)
        this.isColonized = this.planetId === 0 ? Phaser.Math.Between(0, 10) > 3 : Phaser.Math.Between(0, 10) > 7;
        
        // Set planet type
        const types = ['Rocky', 'Gas Giant', 'Ice', 'Terrestrial', 'Desert'];
        this.planetType = types[Phaser.Math.Between(0, types.length - 1)];
        
        // Generate resources and buildings if colonized
        if (this.isColonized) {
            this.generateResources();
            this.generateBuildings();
        }
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
            `${this.planetName} - ${this.systemName}`,
            TextStyles.subtitle
        ).setOrigin(0.5);

        // Planet visualization
        this.createPlanetVisualization(width / 2, height / 3);

        // Back button
        new Button({
            scene: this,
            x: 100,
            y: height - 50,
            text: 'Back to System',
            textStyle: TextStyles.button,
            callback: () => this.backToSystem()
        });

        // Create UI panels
        if (this.isColonized) {
            this.createColonizedUI(width, height);
        } else {
            this.createUncolonizedUI(width, height);
        }
    }

    private createPlanetVisualization(x: number, y: number): void {
        // Planet colors based on type
        const colors: Record<string, number> = {
            'Rocky': 0x888888,
            'Gas Giant': 0x8888ff,
            'Ice': 0xaaddff,
            'Terrestrial': 0x88ff88,
            'Desert': 0xffdd88
        };
        
        // Create planet circle
        const planetSize = 80;
        const planet = this.add.circle(x, y, planetSize, colors[this.planetType] || 0xffffff);
        
        // Add some visual details based on planet type
        if (this.planetType === 'Gas Giant') {
            // Add bands for gas giant
            for (let i = 1; i <= 3; i++) {
                const bandWidth = planetSize * 0.15;
                const bandY = y - planetSize / 2 + i * planetSize / 4;
                this.add.rectangle(x, bandY, planetSize * 2, bandWidth, 0x6666aa, 0.3);
            }
        } else if (this.planetType === 'Terrestrial' || this.planetType === 'Desert') {
            // Add continents for terrestrial/desert
            for (let i = 0; i < 5; i++) {
                const continentSize = Phaser.Math.Between(10, 25);
                const continentX = x + Phaser.Math.Between(-planetSize + 10, planetSize - 10);
                const continentY = y + Phaser.Math.Between(-planetSize + 10, planetSize - 10);
                
                // Make sure continent is within planet circle
                const distFromCenter = Math.sqrt(Math.pow(continentX - x, 2) + Math.pow(continentY - y, 2));
                if (distFromCenter < planetSize - continentSize / 2) {
                    const continentColor = this.planetType === 'Terrestrial' ? 0x338833 : 0xbb8833;
                    this.add.circle(continentX, continentY, continentSize, continentColor);
                }
            }
        } else if (this.planetType === 'Ice') {
            // Add ice caps
            this.add.circle(x, y - planetSize * 0.6, planetSize * 0.4, 0xffffff);
            this.add.circle(x, y + planetSize * 0.6, planetSize * 0.4, 0xffffff);
        }
        
        // Add colonized indicator if applicable
        if (this.isColonized) {
            // Add a small colony indicator
            const colonySize = 15;
            const colony = this.add.rectangle(x + planetSize * 0.6, y - planetSize * 0.6, colonySize, colonySize, 0xffaa00);
            
            // Add a small text label
            this.add.text(
                x + planetSize * 0.6,
                y - planetSize * 0.6 - 15,
                'Colony',
                TextStyles.small
            ).setOrigin(0.5);
        }
        
        // Add planet info text
        this.add.text(
            x,
            y + planetSize + 30,
            `Type: ${this.planetType}\nSize: ${planetSize * 100} km\nGravity: ${(planetSize / 40).toFixed(1)}G`,
            TextStyles.normal
        ).setOrigin(0.5, 0);
    }

    private createColonizedUI(width: number, height: number): void {
        // Resources panel
        const resourcesPanel = new Panel({
            scene: this,
            x: width * 0.25,
            y: height * 0.7,
            width: 300,
            height: 200,
            title: 'Resources'
        });
        
        // Add resources to panel
        let resourceText = '';
        this.resources.forEach(resource => {
            resourceText += `${resource.name}: ${resource.amount} (${resource.production > 0 ? '+' : ''}${resource.production}/turn)\n`;
        });
        
        const resourcesInfo = this.add.text(
            0,
            0,
            resourceText,
            TextStyles.resource
        ).setOrigin(0.5);
        
        resourcesPanel.addContent(resourcesInfo);
        
        // Buildings panel
        const buildingsPanel = new Panel({
            scene: this,
            x: width * 0.75,
            y: height * 0.7,
            width: 300,
            height: 200,
            title: 'Buildings'
        });
        
        // Add buildings to panel
        let buildingsText = '';
        this.buildings.forEach(building => {
            buildingsText += `${building.name} (Lvl ${building.level}): ${building.production}\n`;
        });
        
        const buildingsInfo = this.add.text(
            0,
            0,
            buildingsText || 'No buildings constructed',
            TextStyles.normal
        ).setOrigin(0.5);
        
        buildingsPanel.addContent(buildingsInfo);
        
        // Build button
        const buildButton = new Button({
            scene: this,
            x: 0,
            y: 80,
            text: 'Build New Structure',
            textStyle: TextStyles.button,
            callback: () => this.openBuildMenu()
        });
        
        buildingsPanel.addContent(buildButton);
    }

    private createUncolonizedUI(width: number, height: number): void {
        // Uncolonized info panel
        const infoPanel = new Panel({
            scene: this,
            x: width * 0.5,
            y: height * 0.7,
            width: 400,
            height: 200,
            title: 'Uncolonized Planet'
        });
        
        // Add info to panel
        const infoText = this.add.text(
            0,
            -30,
            'This planet has not been colonized yet. Establish a colony to begin exploiting its resources.',
            TextStyles.normal
        ).setOrigin(0.5, 0);
        infoText.setWordWrapWidth(350);
        
        infoPanel.addContent(infoText);
        
        // Colonize button
        const colonizeButton = new Button({
            scene: this,
            x: 0,
            y: 50,
            text: 'Establish Colony',
            textStyle: TextStyles.button,
            callback: () => this.colonizePlanet()
        });
        
        infoPanel.addContent(colonizeButton);
    }

    private generateResources(): void {
        // Basic resources
        this.resources = [
            { name: 'Minerals', amount: Phaser.Math.Between(100, 500), production: Phaser.Math.Between(5, 20) },
            { name: 'Energy', amount: Phaser.Math.Between(50, 300), production: Phaser.Math.Between(3, 15) },
            { name: 'Food', amount: Phaser.Math.Between(80, 400), production: Phaser.Math.Between(4, 18) }
        ];
        
        // Add special resources based on planet type
        if (this.planetType === 'Gas Giant') {
            this.resources.push({ name: 'Exotic Gases', amount: Phaser.Math.Between(20, 100), production: Phaser.Math.Between(1, 5) });
        } else if (this.planetType === 'Ice') {
            this.resources.push({ name: 'Water Ice', amount: Phaser.Math.Between(50, 200), production: Phaser.Math.Between(2, 8) });
        } else if (this.planetType === 'Desert') {
            this.resources.push({ name: 'Rare Metals', amount: Phaser.Math.Between(10, 50), production: Phaser.Math.Between(1, 3) });
        }
    }

    private generateBuildings(): void {
        // Building types
        const buildingTypes = [
            { name: 'Mine', production: 'Minerals +5/turn', maintenance: 2 },
            { name: 'Power Plant', production: 'Energy +4/turn', maintenance: 1 },
            { name: 'Farm', production: 'Food +6/turn', maintenance: 2 },
            { name: 'Research Lab', production: 'Research +3/turn', maintenance: 3 },
            { name: 'Shipyard', production: 'Ship production +10%', maintenance: 5 }
        ];
        
        // Generate 0-3 buildings
        const buildingCount = Phaser.Math.Between(0, 3);
        
        for (let i = 0; i < buildingCount; i++) {
            const typeIndex = Phaser.Math.Between(0, buildingTypes.length - 1);
            const building: Building = {
                id: i,
                name: buildingTypes[typeIndex].name,
                type: buildingTypes[typeIndex].name.toLowerCase().replace(' ', '_'),
                level: Phaser.Math.Between(1, 3),
                production: buildingTypes[typeIndex].production,
                maintenance: buildingTypes[typeIndex].maintenance
            };
            
            this.buildings.push(building);
        }
    }

    private openBuildMenu(): void {
        console.log('Build menu not implemented yet');
        // In a real game, this would open a build menu with available buildings
    }

    private colonizePlanet(): void {
        console.log('Colonization not implemented yet');
        // In a real game, this would start the colonization process
    }

    private backToSystem(): void {
        this.scene.start('SystemScene', { systemId: this.systemId });
    }
}
