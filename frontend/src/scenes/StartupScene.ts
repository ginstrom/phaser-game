import Phaser from 'phaser';
import Button from '../ui/Button';
import { TextStyles } from '../ui/TextStyles';
import Panel from '../ui/Panel';
import api from '../utils/api';

export default class StartupScene extends Phaser.Scene {
    constructor() {
        super('StartupScene');
    }

    preload() {
        // Preload assets here
        // In a real game, we would load images, sounds, etc.
    }

    create() {
        const { width, height } = this.cameras.main;
        
        // Title
        this.add.text(
            width / 2,
            height * 0.2,
            '4X Space Empire',
            TextStyles.title
        ).setOrigin(0.5);

        // Subtitle
        this.add.text(
            width / 2,
            height * 0.3,
            'A Turn-Based Strategy Game',
            TextStyles.subtitle
        ).setOrigin(0.5);

        // Create buttons
        const buttonSpacing = 70;
        const startY = height * 0.5;

        // New Game button
        new Button({
            scene: this,
            x: width / 2,
            y: startY,
            text: 'New Game',
            textStyle: TextStyles.button,
            callback: () => this.startNewGame()
        });

        // Load Game button
        new Button({
            scene: this,
            x: width / 2,
            y: startY + buttonSpacing,
            text: 'Load Game',
            textStyle: TextStyles.button,
            callback: () => this.loadGame()
        });

        // Settings button
        new Button({
            scene: this,
            x: width / 2,
            y: startY + buttonSpacing * 2,
            text: 'Settings',
            textStyle: TextStyles.button,
            callback: () => this.openSettings()
        });

        // Exit button
        new Button({
            scene: this,
            x: width / 2,
            y: startY + buttonSpacing * 3,
            text: 'Exit',
            textStyle: TextStyles.button,
            callback: () => this.exitGame()
        });

        // Version text
        this.add.text(
            width - 20,
            height - 20,
            'Version 0.1.0',
            TextStyles.small
        ).setOrigin(1);
    }

    private startNewGame(): void {
        console.log('Starting new game');
        
        // Create a panel for the new game dialog
        const { width, height } = this.cameras.main;
        const panel = new Panel({
            scene: this,
            x: width / 2,
            y: height / 2,
            width: 400,
            height: 300,
            title: 'New Game'
        });
        
        // Add player name input field
        const playerNameText = this.add.text(
            width / 2,
            height / 2 - 60,
            'Player Name:',
            TextStyles.normal
        ).setOrigin(0.5);
        
        // Create a default player name
        let playerName = `Player${Math.floor(Math.random() * 1000)}`;
        
        // Add player name display
        const playerNameDisplay = this.add.text(
            width / 2,
            height / 2 - 20,
            playerName,
            { ...TextStyles.normal, color: '#ffff00' }
        ).setOrigin(0.5);
        
        // Add difficulty selection
        const difficultyText = this.add.text(
            width / 2,
            height / 2 + 20,
            'Difficulty: Normal',
            TextStyles.normal
        ).setOrigin(0.5);
        
        let difficulty = 'normal';
        
        // Add galaxy size selection
        const galaxySizeText = this.add.text(
            width / 2,
            height / 2 + 60,
            'Galaxy Size: Medium',
            TextStyles.normal
        ).setOrigin(0.5);
        
        let galaxySize = 'medium';
        
        // Add start button
        const startButton = new Button({
            scene: this,
            x: width / 2,
            y: height / 2 + 120,
            text: 'Start Game',
            textStyle: TextStyles.button,
            callback: async () => {
                // Disable the button to prevent multiple clicks
                startButton.setEnabled(false);
                
                // Show loading text
                const loadingText = this.add.text(
                    width / 2,
                    height / 2 + 160,
                    'Creating game...',
                    TextStyles.normal
                ).setOrigin(0.5);
                
                try {
                    // Call the API to create a new game
                    const response = await api.createNewGame({
                        player_name: playerName,
                        difficulty: difficulty as 'easy' | 'normal' | 'hard',
                        galaxy_size: galaxySize as 'small' | 'medium' | 'large'
                    });
                    
                    console.log('New game created:', response);
                    
                    // Validate response structure
                    if (!response || !response.game_id || !response.initial_state) {
                        throw new Error('Invalid response structure from server');
                    }
                    
                    try {
                        // Store the game state
                        api.GameState.setFromNewGameResponse(response);
                        
                        // Log the game state before transitioning
                        console.log('Game state before transitioning to GalaxyScene:', {
                            gameId: api.GameState.gameId,
                            playerName: api.GameState.playerName,
                            playerEmpire: api.GameState.playerEmpire,
                            resources: api.GameState.resources,
                            galaxySize: api.GameState.galaxySize,
                            galaxySystems: api.GameState.galaxySystems,
                            galaxyExplored: api.GameState.galaxyExplored,
                            turn: api.GameState.turn
                        });
                        
                        // Transition to the galaxy scene
                        this.scene.start('GalaxyScene');
                    } catch (stateError) {
                        console.error('Failed to set game state:', stateError);
                        loadingText.setText('Error initializing game state. Try again.');
                        startButton.setEnabled(true);
                    }
                } catch (error) {
                    console.error('Failed to create new game:', error);
                    
                    // Show error message
                    loadingText.setText('Failed to create game. Try again.');
                    
                    // Re-enable the button
                    startButton.setEnabled(true);
                }
            }
        });
        
        // Add cancel button
        new Button({
            scene: this,
            x: width / 2 - 100,
            y: height / 2 + 120,
            text: 'Cancel',
            textStyle: TextStyles.button,
            callback: () => {
                // Remove all dialog elements
                panel.destroy();
                playerNameText.destroy();
                playerNameDisplay.destroy();
                difficultyText.destroy();
                galaxySizeText.destroy();
                startButton.destroy();
            }
        });
    }

    private loadGame(): void {
        console.log('Load game functionality not implemented yet');
        // In a real game, this would open a load game dialog
    }

    private openSettings(): void {
        console.log('Settings functionality not implemented yet');
        // In a real game, this would open a settings dialog
    }

    private exitGame(): void {
        console.log('Exit game');
        // In a browser, we can't really exit the game, but we could show a confirmation dialog
    }
}
