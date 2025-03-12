import Phaser from 'phaser';
import Button from '../ui/Button';
import Panel from '../ui/Panel';
import { TextStyles } from '../ui/TextStyles';
import { useGameState } from '../state/GameState';

interface CombatUnit {
    id: string;
    type: string;
    position: { x: number; y: number };
    health: number;
    damage: number;
    range: number;
    owner: string;
}

export default class CombatScene extends Phaser.Scene {
    private units: CombatUnit[] = [];
    private selectedUnit: CombatUnit | null = null;
    private infoPanel: Panel | null = null;
    private turnIndicator: Phaser.GameObjects.Text | null = null;

    constructor() {
        super('CombatScene');
    }

    preload() {
        // Load combat-specific assets
        this.load.image('ship_fighter', 'assets/sprites/ships/fighter.png');
        this.load.image('ship_cruiser', 'assets/sprites/ships/cruiser.png');
        this.load.image('ship_battleship', 'assets/sprites/ships/battleship.png');
        this.load.image('combat_background', 'assets/backgrounds/space_battle.png');
    }

    create() {
        const { width, height } = this.cameras.main;

        // Add space background
        this.add.image(0, 0, 'combat_background')
            .setOrigin(0)
            .setDisplaySize(width, height);

        // Initialize combat UI
        this.createUI();
        
        // Initialize combat units
        this.initializeCombatUnits();

        // Add turn indicator
        this.turnIndicator = this.add.text(10, 10, 'Turn: Player 1', TextStyles.panelTitle)
            .setScrollFactor(0);

        // Add control buttons
        this.createControlButtons();
    }

    private createUI() {
        // Create info panel for selected unit
        const panelConfig = {
            scene: this,
            x: this.cameras.main.width - 200,
            y: 10,
            width: 190,
            height: 200,
            title: 'Unit Info'
        };
        this.infoPanel = new Panel(panelConfig);
        this.infoPanel.setVisible(false);
    }

    private initializeCombatUnits() {
        // Initialize combat units (placeholder)
        // This would be populated with actual fleet data from the game state
        const gameState = useGameState.getState();
        // TODO: Add actual fleet initialization
    }

    private createControlButtons() {
        // Add control buttons
        new Button({
            scene: this,
            x: 10,
            y: this.cameras.main.height - 40,
            text: 'End Turn',
            callback: () => this.endTurn()
        });

        new Button({
            scene: this,
            x: 120,
            y: this.cameras.main.height - 40,
            text: 'Retreat',
            callback: () => this.retreat()
        });
    }

    private selectUnit(unit: CombatUnit) {
        this.selectedUnit = unit;
        if (this.infoPanel) {
            this.infoPanel.setVisible(true);
            // Update info panel with unit details
            // TODO: Add actual unit info display
        }
    }

    private endTurn() {
        // Handle end of turn logic
        // TODO: Implement turn handling
    }

    private retreat() {
        // Handle retreat logic
        // TODO: Implement retreat handling
        this.scene.start('GalaxyScene'); // Return to galaxy view
    }

    update() {
        // Handle continuous updates
        // TODO: Implement unit animations and movement
    }
} 