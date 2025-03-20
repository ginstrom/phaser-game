/// <reference path="../../node_modules/phaser/types/phaser.d.ts" />
import Phaser from 'phaser';

interface EmpireData {
    id: number;
    name: string;
    is_human: boolean;
    // Add other empire properties as needed
}

export class EmpireScene extends Phaser.Scene {
    private gameData!: { id: number };
    private empireData!: EmpireData;

    constructor() {
        super({ key: 'EmpireScene' });
    }

    init(data: { gameData: { id: number } }) {
        this.gameData = data.gameData;
    }

    async create(): Promise<void> {
        // Set black background
        this.cameras.main.setBackgroundColor('#000000');

        // Fetch empire data
        try {
            const response = await fetch(`/api/games/${this.gameData.id}/empires/`);
            if (!response.ok) {
                throw new Error('Failed to fetch empires');
            }
            const empires: EmpireData[] = await response.json();
            
            // Find human player's empire
            this.empireData = empires.find(empire => empire.is_human) || empires[0];
            
            // Display empire information
            const title = this.add.text(
                this.cameras.main.centerX,
                50,
                'Empire Information',
                {
                    fontFamily: 'monospace',
                    fontSize: '36px',
                    color: '#00ff00',
                    align: 'center'
                }
            ).setOrigin(0.5);

            // Empire name
            this.add.text(
                this.cameras.main.centerX,
                150,
                `Name: ${this.empireData.name}`,
                {
                    fontFamily: 'monospace',
                    fontSize: '24px',
                    color: '#ffffff',
                    align: 'center'
                }
            ).setOrigin(0.5);

            // Empire ID
            this.add.text(
                this.cameras.main.centerX,
                200,
                `ID: ${this.empireData.id}`,
                {
                    fontFamily: 'monospace',
                    fontSize: '24px',
                    color: '#ffffff',
                    align: 'center'
                }
            ).setOrigin(0.5);

            // Add Galaxy button
            const buttonWidth = 200;
            const buttonHeight = 50;
            const padding = 20;
            const buttonY = this.cameras.main.height - buttonHeight - padding;

            const galaxyButton = this.add.rectangle(
                padding + buttonWidth/2,
                buttonY + buttonHeight/2,
                buttonWidth,
                buttonHeight,
                0x444444
            );
            
            const galaxyButtonText = this.add.text(
                galaxyButton.x,
                galaxyButton.y,
                'Galaxy',
                {
                    fontFamily: 'monospace',
                    fontSize: '24px',
                    color: '#ffffff',
                    align: 'center'
                }
            );
            galaxyButtonText.setOrigin(0.5);

            // Make button interactive
            galaxyButton.setInteractive();
            galaxyButton.on('pointerover', () => {
                galaxyButton.setFillStyle(0x666666);
            });
            galaxyButton.on('pointerout', () => {
                galaxyButton.setFillStyle(0x444444);
            });

            // Button click handler
            galaxyButton.on('pointerdown', () => {
                this.scene.start('GalaxyScene', this.gameData);
            });

        } catch (error) {
            console.error('Error fetching empire data:', error);
            // TODO: Show error message to user
        }
    }
} 