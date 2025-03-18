/// <reference path="../../node_modules/phaser/types/phaser.d.ts" />
import Phaser from 'phaser';

interface GameData {
    id: number;
    turn: number;
    empires: number[];
    systems: number[];
}

export class GalaxyScene extends Phaser.Scene {
    private gameData!: GameData;
    private gameDataText!: Phaser.GameObjects.Text;

    constructor() {
        super({ key: 'GalaxyScene' });
    }

    init(data: GameData) {
        console.log('GalaxyScene init with data:', data);
        this.gameData = data;
    }

    create(): void {
        console.log('GalaxyScene create with gameData:', this.gameData);
        // Set black background
        this.cameras.main.setBackgroundColor('#000000');

        // Display game data
        this.gameDataText = this.add.text(
            10,
            10,
            `Game ID: ${this.gameData.id}\n` +
            `Turn: ${this.gameData.turn}\n` +
            `Empires: ${this.gameData.empires.join(', ')}\n` +
            `Systems: ${this.gameData.systems.join(', ')}`,
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#00ff00',
                align: 'left'
            }
        );

        // Add End Turn button
        const buttonWidth = 200;
        const buttonHeight = 50;
        const padding = 20;
        
        // Position button with its top-left corner at the calculated position
        const buttonX = this.cameras.main.width - buttonWidth - padding;
        const buttonY = this.cameras.main.height - buttonHeight - padding;
        
        const button = this.add.rectangle(
            buttonX + buttonWidth/2,  // Center x
            buttonY + buttonHeight/2, // Center y
            buttonWidth,
            buttonHeight,
            0x444444
        );
        
        const buttonText = this.add.text(
            button.x,
            button.y,
            'End Turn',
            {
                fontFamily: 'monospace',
                fontSize: '24px',
                color: '#ffffff',
                align: 'center'
            }
        );
        buttonText.setOrigin(0.5);

        // Make button interactive
        button.setInteractive();
        button.on('pointerover', () => {
            button.setFillStyle(0x666666);
        });
        button.on('pointerout', () => {
            button.setFillStyle(0x444444);
        });
        button.on('pointerdown', () => this.endTurn());
    }

    private async endTurn(): Promise<void> {
        console.log('Ending turn for game:', this.gameData);
        try {
            const response = await fetch(`/api/games/${this.gameData.id}/end_turn/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('Failed to end turn');
            }

            const updatedGameData = await response.json();
            console.log('Turn ended, updated game data:', updatedGameData);
            this.gameData = updatedGameData;
            this.updateGameDataDisplay();
        } catch (error) {
            console.error('Error ending turn:', error);
            // TODO: Show error message to user
        }
    }

    private updateGameDataDisplay(): void {
        this.gameDataText.setText(
            `Game ID: ${this.gameData.id}\n` +
            `Turn: ${this.gameData.turn}\n` +
            `Empires: ${this.gameData.empires?.join(', ') || 'N/A'}\n` +
            `Systems: ${this.gameData.systems?.join(', ') || 'N/A'}`
        );
    }
} 