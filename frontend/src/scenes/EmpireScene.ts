/// <reference path="../../node_modules/phaser/types/phaser.d.ts" />
import Phaser from 'phaser';
import { SciFiButton, ButtonStyle } from '../ui/buttons/SciFiButton';
import { PhaserTable, PhaserTableColumn } from '../ui/tables/PhaserTable';

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
        const columns: PhaserTableColumn[] = [
            { header: 'Orbit', key: 'orbit', width: 80 },
            { header: 'Type', key: 'type', width: 100 },
            { header: 'Minerals', key: 'mineral', width: 120 },
            { header: 'Organic', key: 'organic', width: 120 },
            { header: 'Radioactive', key: 'radioactive', width: 120 },
            { header: 'Exotic', key: 'exotic', width: 120 }
        ];

        // Transform colonies data to match table format
        const tableData = this.colonies.map(colony => ({
            orbit: colony.orbit,
            type: colony.type,
            mineral: colony.type === 'planet' 
                ? `${colony.mineral_production}\n(${colony.mineral_storage_capacity})`
                : colony.mineral_production,
            organic: colony.type === 'planet'
                ? `${colony.organic_production}\n(${colony.organic_storage_capacity})`
                : colony.organic_production,
            radioactive: colony.type === 'planet'
                ? `${colony.radioactive_production}\n(${colony.radioactive_storage_capacity})`
                : colony.radioactive_production,
            exotic: colony.type === 'planet'
                ? `${colony.exotic_production}\n(${colony.exotic_storage_capacity})`
                : colony.exotic_production
        }));

        // Create and add the table
        const table = new PhaserTable({
            scene: this,
            x: this.cameras.main.width / 2,
            y: 150,
            columns,
            data: tableData,
            cellHeight: 40,
            headerHeight: 48,
            backgroundColor: 0x111111,
            headerBackgroundColor: 0x222222,
            textColor: '#FFFFFF',
            headerTextColor: '#00FF00'
        });

        this.contentContainer?.add(table);
    }

    private showResourcesTab() {
        const columns: PhaserTableColumn[] = [
            { header: 'Resource', key: 'name', width: 150 },
            { header: 'Storage', key: 'storage', width: 200 },
            { header: 'Capacity', key: 'capacity', width: 200 }
        ];

        const tableData = [
            { 
                name: 'Minerals',
                storage: this.empireData.mineral_storage.toString(),
                capacity: this.empireData.resource_capacities.mineral_capacity.toString()
            },
            {
                name: 'Organic',
                storage: this.empireData.organic_storage.toString(),
                capacity: this.empireData.resource_capacities.organic_capacity.toString()
            },
            {
                name: 'Radioactive',
                storage: this.empireData.radioactive_storage.toString(),
                capacity: this.empireData.resource_capacities.radioactive_capacity.toString()
            },
            {
                name: 'Exotic',
                storage: this.empireData.exotic_storage.toString(),
                capacity: this.empireData.resource_capacities.exotic_capacity.toString()
            }
        ];

        // Create and add the table
        const table = new PhaserTable({
            scene: this,
            x: this.cameras.main.width / 2,
            y: 150,
            columns,
            data: tableData,
            cellHeight: 40,
            headerHeight: 48,
            backgroundColor: 0x111111,
            headerBackgroundColor: 0x222222,
            textColor: '#FFFFFF',
            headerTextColor: '#00FF00'
        });

        // Add progress bars after table creation
        tableData.forEach((row, index) => {
            const barWidth = 200;
            const barHeight = 20;
            const barX = table.x - 100;  // Position between Storage and Capacity columns
            const barY = table.y + (index * 40) + 40;  // Adjust based on header height and row height

            // Background bar
            const bgBar = this.add.rectangle(barX, barY, barWidth, barHeight, 0x333333);
            this.contentContainer?.add(bgBar);

            // Fill bar
            const progress = Number(row.storage) / Number(row.capacity);
            if (progress > 0) {
                const fillBar = this.add.rectangle(barX, barY, barWidth * progress, barHeight, 0x00ff00)
                    .setOrigin(0, 0.5);
                this.contentContainer?.add(fillBar);
            }
        });

        this.contentContainer?.add(table);
    }
} 