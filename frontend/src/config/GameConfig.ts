import Phaser from 'phaser';
import { StartupScene } from '../scenes/StartupScene';
import { NewGameScene } from '../scenes/NewGameScene';
import { GalaxyScene } from '../scenes/GalaxyScene';
import { EmpireScene } from '../scenes/EmpireScene';

export const GameConfig: Phaser.Types.Core.GameConfig = {
    type: Phaser.AUTO,
    width: 1024,
    height: 768,
    backgroundColor: '#000000',
    parent: 'game',
    scene: [StartupScene, NewGameScene, GalaxyScene, EmpireScene],
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { x: 0, y: 0 },
            debug: false
        }
    }
}; 