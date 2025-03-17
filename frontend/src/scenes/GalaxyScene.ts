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

    constructor() {
        super({ key: 'GalaxyScene' });
    }

    init(data: GameData) {
        this.gameData = data;
    }

    create() {
        // Set black background
        this.cameras.main.setBackgroundColor('#000000');

        // Display game data
        const gameDataText = this.add.text(
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
    }
} 