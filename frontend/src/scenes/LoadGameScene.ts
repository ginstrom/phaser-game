import Phaser from 'phaser';
import { SciFiButton, ButtonStyle } from '../ui/buttons/SciFiButton';
import { PhaserTable, PhaserTableConfig } from '../ui/tables/PhaserTable';

interface GameData {
    id: number;
    turn: number;
    created: string;
    modified: string;
}

export class LoadGameScene extends Phaser.Scene {
    private gamesTable!: PhaserTable;
    private games: GameData[] = [];

    constructor() {
        super({ key: 'LoadGameScene' });
    }

    async create(): Promise<void> {
        // Set black background
        this.cameras.main.setBackgroundColor('#000000');

        // Create title
        const title = this.add.text(
            this.cameras.main.centerX,
            50,
            'Load Game',
            {
                fontFamily: 'monospace',
                fontSize: '36px',
                color: '#00ff00',
                align: 'center'
            }
        ).setOrigin(0.5);

        // Add glowing effect to title
        this.tweens.add({
            targets: title,
            alpha: { from: 0.7, to: 1 },
            duration: 1500,
            ease: 'Sine.InOut',
            yoyo: true,
            repeat: -1
        });

        // Create Back button
        new SciFiButton({
            scene: this,
            x: 100,
            y: this.cameras.main.height - 50,
            text: 'Back',
            style: ButtonStyle.SECONDARY,
            callback: () => {
                if (this.gamesTable) {
                    this.gamesTable.destroy();
                }
                this.scene.start('StartupScene');
            }
        });

        // Load and display games
        await this.loadGames();
    }

    private async loadGames(): Promise<void> {
        try {
            const response = await fetch('/api/games/');
            if (!response.ok) {
                throw new Error('Failed to fetch games');
            }

            this.games = await response.json();
            this.displayGames();
        } catch (error) {
            console.error('Error loading games:', error);
            // TODO: Show error message to user
        }
    }

    private displayGames(): void {
        // Format dates for display
        const formatDate = (dateStr: string) => {
            const date = new Date(dateStr);
            return date.toLocaleString();
        };

        // Create action buttons for each row
        const createActions = (game: GameData) => {
            const container = new Phaser.GameObjects.Container(this, 0, 0);

            // Load button
            const loadButton = new SciFiButton({
                scene: this,
                x: -50,
                y: 0,
                text: 'Load',
                width: 80,
                height: 30,
                style: ButtonStyle.PRIMARY,
                textStyle: { fontSize: '14px' },
                callback: () => {
                    if (this.gamesTable) {
                        this.gamesTable.destroy();
                    }
                    this.scene.start('GalaxyScene', game);
                }
            });

            // Delete button
            const deleteButton = new SciFiButton({
                scene: this,
                x: 50,
                y: 0,
                text: 'Delete',
                width: 80,
                height: 30,
                style: ButtonStyle.DANGER,
                textStyle: { fontSize: '14px' },
                callback: async () => {
                    try {
                        const response = await fetch(`/api/games/${game.id}/`, {
                            method: 'DELETE'
                        });
                        if (!response.ok) {
                            throw new Error('Failed to delete game');
                        }
                        // Reload games list
                        await this.loadGames();
                    } catch (error) {
                        console.error('Error deleting game:', error);
                        // TODO: Show error message to user
                    }
                }
            });

            container.add([loadButton, deleteButton]);
            return container;
        };

        // If table exists, destroy it before creating a new one
        if (this.gamesTable) {
            this.gamesTable.destroy();
            this.gamesTable = null!;
        }

        // Configure table
        const config: PhaserTableConfig = {
            scene: this,
            x: this.cameras.main.centerX,
            y: 150,
            columns: [
                { header: 'ID', key: 'id', width: 100 },
                { header: 'Turn', key: 'turn', width: 100 },
                { header: 'Created', key: 'created', width: 200, formatter: formatDate },
                { header: 'Modified', key: 'modified', width: 200, formatter: formatDate },
                { header: 'Actions', key: 'actions', width: 200 }
            ],
            data: this.games.map(game => ({
                ...game,
                actions: createActions(game)
            })),
            cellHeight: 40,
            headerHeight: 50,
            backgroundColor: 0x111111,
            headerBackgroundColor: 0x222222,
            textColor: '#FFFFFF',
            headerTextColor: '#00FF00'
        };

        // Create table
        this.gamesTable = new PhaserTable(config);
    }
} 