/// <reference path="../../node_modules/phaser/types/phaser.d.ts" />
import Phaser from 'phaser';

interface GameData {
    id: number;
    turn: number;
    empires: number[];
    systems: number[];
}

interface StarData {
    id: number;
    star_type: string;
}

interface PlanetData {
    id: number;
    orbit: number;
    empire_id: number | null;
    mineral_production: number;
    organic_production: number;
    radioactive_production: number;
    exotic_production: number;
    mineral_storage_capacity: number;
    organic_storage_capacity: number;
    radioactive_storage_capacity: number;
    exotic_storage_capacity: number;
}

interface AsteroidBeltData {
    id: number;
    orbit: number;
    empire_id: number | null;
    mineral_production: number;
    organic_production: number;
    radioactive_production: number;
    exotic_production: number;
}

interface SystemData {
    id: number;
    x: number;
    y: number;
    name: string | null;
    empire_id: number | null;
    star: StarData;
    planets: PlanetData[];
    asteroid_belts: AsteroidBeltData[];
}

export class GalaxyScene extends Phaser.Scene {
    private gameData!: GameData;
    private turnText!: Phaser.GameObjects.Text;
    private systems: SystemData[] = [];
    private readonly GRID_SIZE = 50;
    private readonly PADDING = 50; // Padding from screen edges

    constructor() {
        super({ key: 'GalaxyScene' });
    }

    init(data: GameData) {
        this.gameData = data;
    }

    async create(): Promise<void> {
        // Set black background
        this.cameras.main.setBackgroundColor('#000000');

        // Calculate UI dimensions
        const buttonWidth = 200;
        const buttonHeight = 50;
        const padding = 20;
        const topBarHeight = 60; // Height for the top bar containing turn number
        const bottomBarHeight = buttonHeight + (padding * 2); // Height for the bottom bar containing buttons

        // Display turn number in top right, above the grid
        this.turnText = this.add.text(
            this.cameras.main.width - padding,
            padding,
            `Turn: ${this.gameData.turn}`,
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#00ff00',
                align: 'right'
            }
        );
        this.turnText.setOrigin(1, 0);

        // Adjust PADDING to account for top and bottom bars
        const effectivePadding = {
            top: this.PADDING + topBarHeight,
            bottom: this.PADDING + bottomBarHeight,
            left: this.PADDING,
            right: this.PADDING
        };

        // Draw grid with adjusted padding
        this.drawGrid(effectivePadding);

        // Fetch and draw systems with adjusted padding
        await this.fetchAndDrawSystems(effectivePadding);
        
        // Position End Turn button in bottom right
        const endTurnButtonX = this.cameras.main.width - buttonWidth - padding;
        const buttonY = this.cameras.main.height - buttonHeight - padding;
        
        const endTurnButton = this.add.rectangle(
            endTurnButtonX + buttonWidth/2,
            buttonY + buttonHeight/2,
            buttonWidth,
            buttonHeight,
            0x444444
        );
        
        const endTurnButtonText = this.add.text(
            endTurnButton.x,
            endTurnButton.y,
            'End Turn',
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#ffffff',
                align: 'center'
            }
        );
        endTurnButtonText.setOrigin(0.5);

        // Add Empire button in bottom right, before Exit button
        const empireButton = this.add.rectangle(
            endTurnButtonX - buttonWidth - padding + buttonWidth/2,
            buttonY + buttonHeight/2,
            buttonWidth,
            buttonHeight,
            0x444444
        );
        
        const empireButtonText = this.add.text(
            empireButton.x,
            empireButton.y,
            'Empire',
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#ffffff',
                align: 'center'
            }
        );
        empireButtonText.setOrigin(0.5);

        // Add Exit button in bottom left
        const exitButton = this.add.rectangle(
            padding + buttonWidth/2,
            buttonY + buttonHeight/2,
            buttonWidth,
            buttonHeight,
            0x444444
        );
        
        const exitButtonText = this.add.text(
            exitButton.x,
            exitButton.y,
            'Exit',
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#ffffff',
                align: 'center'
            }
        );
        exitButtonText.setOrigin(0.5);

        // Make buttons interactive
        [endTurnButton, empireButton, exitButton].forEach(button => {
            button.setInteractive();
            button.on('pointerover', () => {
                button.setFillStyle(0x666666);
            });
            button.on('pointerout', () => {
                button.setFillStyle(0x444444);
            });
        });

        // Button click handlers
        endTurnButton.on('pointerdown', () => this.endTurn());
        empireButton.on('pointerdown', () => {
            this.scene.start('EmpireScene', { gameData: this.gameData });
        });
        exitButton.on('pointerdown', () => {
            this.scene.start('StartupScene');
        });
    }

    private drawGrid(padding: { top: number, bottom: number, left: number, right: number }): void {
        const graphics = this.add.graphics();
        graphics.lineStyle(1, 0x333333);

        // Calculate grid dimensions with adjusted padding
        const gridWidth = this.cameras.main.width - (padding.left + padding.right);
        const gridHeight = this.cameras.main.height - (padding.top + padding.bottom);
        const cellWidth = gridWidth / this.GRID_SIZE;
        const cellHeight = gridHeight / this.GRID_SIZE;

        // Draw vertical lines
        for (let x = 0; x <= this.GRID_SIZE; x++) {
            const xPos = padding.left + (x * cellWidth);
            graphics.moveTo(xPos, padding.top);
            graphics.lineTo(xPos, this.cameras.main.height - padding.bottom);
        }

        // Draw horizontal lines
        for (let y = 0; y <= this.GRID_SIZE; y++) {
            const yPos = padding.top + (y * cellHeight);
            graphics.moveTo(padding.left, yPos);
            graphics.lineTo(this.cameras.main.width - padding.right, yPos);
        }

        graphics.strokePath();
    }

    private async fetchAndDrawSystems(padding: { top: number, bottom: number, left: number, right: number }): Promise<void> {
        try {
            // Fetch all systems for this game
            const response = await fetch(`/api/games/${this.gameData.id}/systems/`);
            if (!response.ok) {
                throw new Error('Failed to fetch systems');
            }
            this.systems = await response.json();
            console.log('Fetched systems:', this.systems);

            // Calculate grid dimensions with adjusted padding
            const gridWidth = this.cameras.main.width - (padding.left + padding.right);
            const gridHeight = this.cameras.main.height - (padding.top + padding.bottom);
            const cellWidth = gridWidth / this.GRID_SIZE;
            const cellHeight = gridHeight / this.GRID_SIZE;
            console.log('Grid dimensions:', { gridWidth, gridHeight, cellWidth, cellHeight });

            // Draw each system
            this.systems.forEach(system => {
                // Calculate position on grid with adjusted padding
                const x = padding.left + (system.x * cellWidth);
                const y = padding.top + (system.y * cellHeight);
                const radius = Math.min(cellWidth, cellHeight) * 0.4;
                console.log('Drawing system:', { system, x, y, radius });

                // Draw system circle with star color
                const starColor = this.getStarColor(system.star.star_type);
                const circle = this.add.circle(x, y, radius, starColor);
                
                // Add system name
                const nameText = this.add.text(x, y - radius - 5, system.name || `System ${system.id}`, {
                    fontFamily: 'monospace',
                    fontSize: '12px',
                    color: '#ffffff',
                    align: 'center'
                });
                nameText.setOrigin(0.5);

                // Make system interactive
                circle.setInteractive();
                circle.on('pointerover', () => {
                    circle.setFillStyle(0x666666);
                });
                circle.on('pointerout', () => {
                    circle.setFillStyle(starColor);
                });
            });
        } catch (error) {
            console.error('Error fetching systems:', error);
            // TODO: Show error message to user
        }
    }

    private getStarColor(starType: string): number {
        switch (starType.toLowerCase()) {
            case 'blue':
                return 0x4444ff;
            case 'white':
                return 0xffffff;
            case 'yellow':
                return 0xffff00;
            case 'orange':
                return 0xff8800;
            case 'brown':
                return 0x884400;
            default:
                return 0x444444;
        }
    }

    private async endTurn(): Promise<void> {
        try {
            const response = await fetch(`/api/games/${this.gameData.id}/end-turn/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Failed to end turn');
            }

            const updatedGameData = await response.json();
            this.gameData = updatedGameData;
            this.turnText.setText(`Turn: ${this.gameData.turn}`);
            
            // Calculate UI dimensions for padding
            const buttonHeight = 50;
            const padding = 20;
            const topBarHeight = 60;
            const bottomBarHeight = buttonHeight + (padding * 2);

            // Create padding object for grid and systems
            const effectivePadding = {
                top: this.PADDING + topBarHeight,
                bottom: this.PADDING + bottomBarHeight,
                left: this.PADDING,
                right: this.PADDING
            };
            
            // Refresh systems after turn with proper padding
            await this.fetchAndDrawSystems(effectivePadding);
        } catch (error) {
            console.error('Error ending turn:', error);
            // TODO: Show error message to user
        }
    }
} 