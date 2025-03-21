/// <reference path="../../node_modules/phaser/types/phaser.d.ts" />
import Phaser from 'phaser';
import { SciFiButton, ButtonStyle } from '../ui/buttons/SciFiButton';

interface PlayerData {
    id: number;
    player_type: 'human' | 'computer';
}

interface RaceData {
    id: number;
    name: string;
}

interface ResourceCapacities {
    mineral_capacity: number;
    organic_capacity: number;
    radioactive_capacity: number;
    exotic_capacity: number;
}

interface EmpireData {
    id: number;
    name: string;
    player: PlayerData;
    race: RaceData;
    game: number;
    planets: Colony[];
    asteroid_belts: Colony[];
    mineral_storage: number;
    organic_storage: number;
    radioactive_storage: number;
    exotic_storage: number;
    resource_capacities: ResourceCapacities;
}

interface BaseColony {
    id: number;
    mineral_production: string;
    organic_production: string;
    radioactive_production: string;
    exotic_production: string;
    orbit: number;
}

interface Planet extends BaseColony {
    type: 'planet';
    mineral_storage_capacity: string;
    organic_storage_capacity: string;
    radioactive_storage_capacity: string;
    exotic_storage_capacity: string;
}

interface AsteroidBelt extends BaseColony {
    type: 'asteroid-belt';
}

type Colony = Planet | AsteroidBelt;

export class EmpireScene extends Phaser.Scene {
    private gameData!: { id: number };
    private empireData!: EmpireData;
    private activeTab: string = 'colonies';
    private colonies: Colony[] = [];
    private contentContainer?: Phaser.GameObjects.Container;

    constructor() {
        super({ key: 'EmpireScene' });
    }

    init(data: { gameData: { id: number } }) {
        this.gameData = data.gameData;
    }

    async create(): Promise<void> {
        // Set black background
        this.cameras.main.setBackgroundColor('#000000');

        // Calculate UI dimensions
        const buttonWidth = 200;
        const buttonHeight = 50;
        const padding = 20;

        // Create container for tab content
        this.contentContainer = this.add.container(0, 100); // Move container down to avoid overlap with tabs

        // Create tab buttons with consistent styling
        const tabY = 50;
        const tabWidth = 150;
        const tabSpacing = 10;

        // Create colonies tab button
        new SciFiButton({
            scene: this,
            x: 50 + (tabWidth/2),
            y: tabY,
            text: 'Colonies',
            width: tabWidth,
            style: this.activeTab === 'colonies' ? ButtonStyle.PRIMARY : ButtonStyle.SECONDARY,
            callback: () => this.switchTab('colonies')
        });

        // Create resources tab button
        new SciFiButton({
            scene: this,
            x: 50 + tabWidth + tabSpacing + (tabWidth/2),
            y: tabY,
            text: 'Resources',
            width: tabWidth,
            style: this.activeTab === 'resources' ? ButtonStyle.PRIMARY : ButtonStyle.SECONDARY,
            callback: () => this.switchTab('resources')
        });

        // Create Galaxy button in bottom right
        new SciFiButton({
            scene: this,
            x: this.cameras.main.width - buttonWidth/2 - padding,
            y: this.cameras.main.height - buttonHeight/2 - padding,
            text: 'Galaxy',
            width: buttonWidth,
            style: ButtonStyle.SECONDARY,
            callback: () => {
                this.scene.start('GalaxyScene', { ...this.gameData });
            }
        });

        // Load empire data and show initial tab
        await this.loadEmpireData();
        this.showColoniesTab();
    }

    private async loadEmpireData() {
        try {
            // First get the game data to find our empire
            const gameResponse = await fetch(`/api/games/${this.gameData.id}/empires/`);
            if (!gameResponse.ok) {
                throw new Error('Failed to fetch game empires');
            }
            const empires: EmpireData[] = await gameResponse.json();
            const humanEmpire = empires.find(empire => empire.player.player_type === 'human');
            if (!humanEmpire) {
                throw new Error('Could not find human empire');
            }

            // Now get the detailed empire data
            const empireResponse = await fetch(`/api/empires/${humanEmpire.id}/`);
            if (!empireResponse.ok) {
                throw new Error('Failed to fetch empire data');
            }
            this.empireData = await empireResponse.json();
            
            // Fetch planets and asteroid belts using the correct empire ID
            const [planetsResponse, asteroidsResponse] = await Promise.all([
                fetch(`/api/empires/${this.empireData.id}/planets/`),
                fetch(`/api/empires/${this.empireData.id}/asteroid-belts/`)
            ]);

            if (!planetsResponse.ok || !asteroidsResponse.ok) {
                throw new Error('Failed to fetch colonies data');
            }

            const planets = await planetsResponse.json();
            const asteroids = await asteroidsResponse.json();

            this.colonies = [
                ...planets.map((p: any) => ({ ...p, type: 'planet' as const })),
                ...asteroids.map((a: any) => ({ ...a, type: 'asteroid-belt' as const }))
            ];

            // Sort colonies by orbit number
            this.colonies.sort((a, b) => a.orbit - b.orbit);
        } catch (error) {
            console.error('Failed to load empire data:', error);
            // TODO: Show error message to user
        }
    }

    private switchTab(tab: string) {
        this.activeTab = tab;
        
        // Clear previous content by destroying all children
        if (this.contentContainer) {
            this.contentContainer.removeAll(true);
        }
        
        // Update tab visuals and show appropriate content
        if (tab === 'colonies') {
            this.showColoniesTab();
        } else {
            this.showResourcesTab();
        }
    }

    private showColoniesTab() {
        const startY = 20; // Adjusted since container is moved down
        const rowHeight = 40;
        const colWidths = [80, 100, 120, 120, 120, 120];
        
        // Headers
        const headers = ['Orbit', 'Type', 'Minerals', 'Organic', 'Radioactive', 'Exotic'];
        headers.forEach((header, i) => {
            const x = 50 + (i > 0 ? colWidths.slice(0, i).reduce((a, b) => a + b, 0) : 0);
            this.contentContainer?.add(
                this.add.text(x, startY, header, {
                    fontSize: '20px',
                    color: '#00ff00',
                    fontFamily: 'monospace'
                })
            );
        });

        // Data rows
        this.colonies.forEach((colony, index) => {
            const y = startY + rowHeight + (index * rowHeight);
            let xPos = 50;

            // Orbit
            this.contentContainer?.add(
                this.add.text(xPos, y, colony.orbit.toString(), {
                    fontSize: '18px',
                    color: '#ffffff',
                    fontFamily: 'monospace'
                })
            );
            xPos += colWidths[0];

            // Type
            this.contentContainer?.add(
                this.add.text(xPos, y, colony.type, {
                    fontSize: '18px',
                    color: '#ffffff',
                    fontFamily: 'monospace'
                })
            );
            xPos += colWidths[1];

            // Production values
            const productions = [
                { value: colony.mineral_production, capacity: colony.type === 'planet' ? colony.mineral_storage_capacity : undefined },
                { value: colony.organic_production, capacity: colony.type === 'planet' ? colony.organic_storage_capacity : undefined },
                { value: colony.radioactive_production, capacity: colony.type === 'planet' ? colony.radioactive_storage_capacity : undefined },
                { value: colony.exotic_production, capacity: colony.type === 'planet' ? colony.exotic_storage_capacity : undefined }
            ];

            productions.forEach((prod, i) => {
                const text = prod.capacity 
                    ? `${prod.value}\n(${prod.capacity})`
                    : prod.value;
                
                this.contentContainer?.add(
                    this.add.text(xPos, y, text, {
                        fontSize: '16px',
                        color: '#ffffff',
                        fontFamily: 'monospace',
                        align: 'center'
                    })
                );
                xPos += colWidths[i + 2];
            });
        });
    }

    private showResourcesTab() {
        const startY = 120;
        const rowHeight = 30;
        
        // Current Storage
        this.contentContainer?.add(
            this.add.text(50, startY, 'Current Storage', {
                fontSize: '24px',
                color: '#00ff00',
                fontFamily: 'monospace'
            })
        );

        const resources = [
            { name: 'Minerals', current: this.empireData.mineral_storage, capacity: this.empireData.resource_capacities.mineral_capacity },
            { name: 'Organic', current: this.empireData.organic_storage, capacity: this.empireData.resource_capacities.organic_capacity },
            { name: 'Radioactive', current: this.empireData.radioactive_storage, capacity: this.empireData.resource_capacities.radioactive_capacity },
            { name: 'Exotic', current: this.empireData.exotic_storage, capacity: this.empireData.resource_capacities.exotic_capacity }
        ];

        resources.forEach((resource, index) => {
            const y = startY + 40 + (index * rowHeight);
            
            // Resource name
            this.contentContainer?.add(
                this.add.text(50, y, resource.name, {
                    fontSize: '18px',
                    color: '#ffffff',
                    fontFamily: 'monospace'
                })
            );

            // Current / Capacity
            this.contentContainer?.add(
                this.add.text(200, y, `${resource.current} / ${resource.capacity}`, {
                    fontSize: '18px',
                    color: '#ffffff',
                    fontFamily: 'monospace'
                })
            );

            // Storage bar
            const barWidth = 200;
            const barHeight = 20;
            const percentage = resource.capacity > 0 ? (resource.current / resource.capacity) : 0;
            
            // Background bar
            this.contentContainer?.add(
                this.add.rectangle(400, y + 10, barWidth, barHeight, 0x333333)
            );
            
            // Fill bar
            if (percentage > 0) {
                this.contentContainer?.add(
                    this.add.rectangle(400, y + 10, barWidth * percentage, barHeight, 0x00ff00)
                        .setOrigin(0, 0.5)
                );
            }
        });
    }
} 