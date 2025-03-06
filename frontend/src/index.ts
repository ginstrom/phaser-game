import Phaser from 'phaser';
import MainScene from './scenes/MainScene';
import StartupScene from './scenes/StartupScene';
import GalaxyScene from './scenes/GalaxyScene';
import SystemScene from './scenes/SystemScene';
import PlanetScene from './scenes/PlanetScene';

// Game configuration
const config: Phaser.Types.Core.GameConfig = {
    type: Phaser.AUTO,
    width: 1024,
    height: 768,
    parent: 'game-container',
    backgroundColor: '#000000',
    scene: [StartupScene, GalaxyScene, SystemScene, PlanetScene, MainScene],
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { x: 0, y: 0 },
            debug: false
        }
    }
};

// Initialize the game
const game = new Phaser.Game(config);
